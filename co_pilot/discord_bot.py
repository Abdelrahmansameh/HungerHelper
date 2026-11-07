import os
import sys
import glob
import re
import subprocess

# Register NVIDIA CUDA 12 and cuDNN DLL directories on Windows (must be first)
_site_packages = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages")
_nvidia_dir = os.path.join(_site_packages, "nvidia")
if os.path.exists(_nvidia_dir):
    for _bin_dir in glob.glob(_nvidia_dir + "/**/bin", recursive=True):
        try:
            os.add_dll_directory(_bin_dir)
        except Exception:
            pass
        os.environ["PATH"] = _bin_dir + os.pathsep + os.environ["PATH"]

import time
import threading
import asyncio
import json
from typing import Optional, Dict
import discord
from discord import app_commands
from discord.ext import commands, tasks
import edge_tts
import imageio_ffmpeg
from co_pilot.brain import CoPilotBrain
from co_pilot.profile_store import get_user_progression_summary
from co_pilot.audio_output import speak_async, stop_audio
from co_pilot.mic_listener import LocalMicListener
from discord.ext import voice_recv
from co_pilot.discord_voice_listener import DiscordSquadVoiceSink

# Ensure Opus library is loaded for Discord voice transmit/receive
if not discord.opus.is_loaded():
    discord.opus._load_default()
    print(f"[Discord Voice Core] Opus encoder loaded: {discord.opus.is_loaded()}", flush=True)

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
TTS_VOICE = os.getenv("TTS_VOICE", "fr-FR-VivienneMultilingualNeural")
WAKE_WORDS = ["eloise", "heloise", "eloïse", "éloïse", "héloïse"]

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
brain = CoPilotBrain()

# Active voice client per guild
active_voice_clients: Dict[int, discord.VoiceClient] = {}
# Active squad voice listener sinks per guild
active_voice_sinks: Dict[int, DiscordSquadVoiceSink] = {}
# Guild voice playback locks to prevent overlapping speech
_guild_voice_locks: Dict[int, asyncio.Lock] = {}
# Global reference to live mic listener instance
mic_listener_instance: Optional[LocalMicListener] = None

def get_guild_voice_lock(guild_id: int) -> asyncio.Lock:
    if guild_id not in _guild_voice_locks:
        _guild_voice_locks[guild_id] = asyncio.Lock()
    return _guild_voice_locks[guild_id]

def stop_all_speech():
    """Instantly cuts off audio in both the PC headset and Discord voice channel."""
    stop_audio()
    for guild_id, vc in list(active_voice_clients.items()):
        if vc and vc.is_connected() and vc.is_playing():
            try:
                vc.stop()
            except Exception:
                pass

# Single live status message reference in #hunger-helper
latest_mic_message: Optional[discord.Message] = None
# Separate reference for the wake confirmation message (prevents it blocking command results)
latest_wake_message: Optional[discord.Message] = None
# Active command window timestamp
active_command_window: float = 0.0

# Thread pool for running brain processing off the audio callback thread
_brain_executor = threading.Thread  # We use asyncio.create_task with run_in_executor pattern

# ---------------------------------------------------------------------------
# UTILITY HELPERS
# ---------------------------------------------------------------------------

def find_target_channel(guild: discord.Guild) -> Optional[discord.TextChannel]:
    """Strictly find the #hunger or #hunger-helper text channel."""
    # 1. Exact match for hunger or hunger-helper
    for ch in guild.text_channels:
        if ch.name.lower() in ["hunger", "hunger-helper"]:
            return ch
    # 2. Contains hunger
    for ch in guild.text_channels:
        clean_name = ch.name.lower().replace("-", "").replace("_", "")
        if "hunger" in clean_name:
            return ch
    for ch in guild.text_channels:
        if ch.permissions_for(guild.me).send_messages:
            return ch
    return None

_TTS_CACHE: Dict[str, str] = {}

async def generate_speech_wav(text: str, filename_prefix: str = "copilot_speech") -> str:
    """Synthesize audio and convert directly to clean 48kHz 16-bit stereo PCM WAV for zero-distortion Discord playback."""
    temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "temp_audio"))
    os.makedirs(temp_dir, exist_ok=True)

    cache_key = f"{TTS_VOICE}_{text.strip().lower()}"
    if cache_key in _TTS_CACHE and os.path.exists(_TTS_CACHE[cache_key]):
        return _TTS_CACHE[cache_key]

    t_id = int(time.time() * 1000)
    mp3_path = os.path.join(temp_dir, f"{filename_prefix}_{t_id}.mp3")
    wav_path = os.path.join(temp_dir, f"{filename_prefix}_{t_id}.wav")

    comm = edge_tts.Communicate(text, TTS_VOICE)
    await comm.save(mp3_path)

    # Convert to pure 48kHz stereo uncompressed PCM WAV
    cmd = [FFMPEG_EXE, "-y", "-i", mp3_path, "-ar", "48000", "-ac", "2", "-f", "wav", wav_path]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    try:
        if os.path.exists(mp3_path):
            os.remove(mp3_path)
    except OSError:
        pass

    _TTS_CACHE[cache_key] = wav_path
    return wav_path

async def play_voice_response(guild_id: int, text: str):
    """Play loud, clear spoken response in the connected Discord voice channel without cutting off."""
    if not text or not text.strip():
        return
    vc = active_voice_clients.get(guild_id)
    if not vc or not vc.is_connected():
        return

    clean = re.sub(r"[\*#_~`\|]+", " ", text)
    clean = re.sub(r"[^\w\s\.,\?!'-]", " ", clean).strip()
    clean = re.sub(r"\s+", " ", clean).strip()
    if not clean or len(clean) < 1:
        return

    try:
        wav_file = await generate_speech_wav(clean, f"speech_{guild_id}")
        if not wav_file or not os.path.exists(wav_file):
            return

        audio_source = discord.FFmpegPCMAudio(
            executable=FFMPEG_EXE,
            source=wav_file
        )
        # Volume boost to 1.8x so it is loud and clearly audible over gunfire and raid effects
        vol_source = discord.PCMVolumeTransformer(audio_source, volume=1.8)

        lock = get_guild_voice_lock(guild_id)
        async with lock:
            if vc.is_playing():
                vc.stop()
                await asyncio.sleep(0.04)

            vc.play(vol_source)
            print(f"[Eloise Discord Voice (LOUD)]: \"{clean}\"", flush=True)

            while vc.is_playing():
                await asyncio.sleep(0.05)

    except Exception as e:
        print(f"[Voice Output Error]: {e}", flush=True)

async def safe_update_status(channel: discord.TextChannel, content: str,
                              message_ref_name: str) -> Optional[discord.Message]:
    """Edit the existing status message or send a new one. Returns the message."""
    global latest_mic_message, latest_wake_message
    try:
        ref = latest_mic_message if message_ref_name == "mic" else latest_wake_message
        if ref and ref.channel.id == channel.id:
            try:
                await ref.edit(content=content)
                return ref
            except Exception:
                pass
        msg = await channel.send(content)
        if message_ref_name == "mic":
            latest_mic_message = msg
        else:
            latest_wake_message = msg
        return msg
    except discord.Forbidden:
        print(f"[Discord Permission Warning] Lacking 'Send Messages' in #{channel.name}. Check role permissions.", flush=True)
        return None
    except Exception as e:
        print(f"[Discord Status Update Error in #{channel.name}]: {e}", flush=True)
        return None

# ---------------------------------------------------------------------------
# VOICE CHANNEL MANAGEMENT
# ---------------------------------------------------------------------------

def is_eloise_active_in_hunger() -> bool:
    """Strictly returns True ONLY if Eloise is currently connected to the voice channel named HUNGER."""
    for guild_id, vc in list(active_voice_clients.items()):
        if vc and vc.is_connected() and vc.channel:
            if vc.channel.name.strip().upper() == "HUNGER":
                return True
    return False

async def post_squad_intel_to_chat(guild: discord.Guild, uid: int, username: str, display: str, img_path: Optional[str]):
    """Post rich tactical card & display response to #hunger tagging the squadmate who asked."""
    target_ch = find_target_channel(guild)
    if not target_ch:
        return

    content = f"<@{uid}> ⚔️ **Eloise :**\n{display}" if display else f"<@{uid}>"
    file_to_send = None
    if img_path and os.path.exists(img_path):
        file_to_send = discord.File(img_path)

    try:
        if file_to_send:
            await target_ch.send(content=content, file=file_to_send)
        else:
            await target_ch.send(content=content)
    except Exception as e:
        print(f"[Post Intel Error in #{target_ch.name}]: {e}", flush=True)

async def auto_join_active_voice(guild: discord.Guild) -> Optional[discord.VoiceClient]:
    """Strictly connect ONLY to the voice channel named HUNGER when players are in it."""
    target_vc = None
    for vc in guild.voice_channels:
        if vc.name.strip().upper() == "HUNGER":
            target_vc = vc
            break

    if not target_vc:
        return None

    # Check connect permissions
    perms = target_vc.permissions_for(guild.me)
    if not perms.connect:
        print(f"[Voice Permission Warning] Eloise lacks 'Connect' permission for voice channel '{target_vc.name}'! Please grant role permissions in Discord.", flush=True)
        return None

    humans = [m for m in target_vc.members if not m.bot]
    current_vc = guild.voice_client

    if not humans:
        if current_vc and current_vc.is_connected():
            ch_name = current_vc.channel.name
            if guild.id in active_voice_sinks:
                try:
                    active_voice_sinks[guild.id].cleanup()
                    active_voice_sinks.pop(guild.id, None)
                except Exception:
                    pass
            await current_vc.disconnect()
            active_voice_clients.pop(guild.id, None)
            print(f"[Voice] Nobody in HUNGER. Eloise disconnected from: {ch_name}", flush=True)
        return None

    if current_vc and current_vc.is_connected():
        if current_vc.channel.id != target_vc.id:
            await current_vc.move_to(target_vc)
            active_voice_clients[guild.id] = current_vc
            print(f"[Voice] Moved to channel: {target_vc.name}", flush=True)
        return active_voice_clients.get(guild.id)
    else:
        try:
            # Clean up any lingering or zombie voice connection before connecting
            if current_vc:
                try:
                    await current_vc.disconnect(force=True)
                except Exception:
                    pass
            active_voice_clients.pop(guild.id, None)

            # Connect using full-duplex VoiceRecvClient to hear squadmates and speak simultaneously!
            vc = await target_vc.connect(cls=voice_recv.VoiceRecvClient, reconnect=True, timeout=12.0)
            active_voice_clients[guild.id] = vc
            print(f"[Voice] Eloise connected to: {target_vc.name} (Full-Duplex Multi-User Voice Receiver)", flush=True)

            # Start squad voice listener sink
            if guild.id in active_voice_sinks:
                try:
                    active_voice_sinks[guild.id].cleanup()
                except Exception:
                    pass
            squad_sink = DiscordSquadVoiceSink(bot, guild, brain, play_voice_response, post_squad_intel_to_chat)
            active_voice_sinks[guild.id] = squad_sink
            vc.listen(squad_sink)

            await asyncio.sleep(0.8)
            greeting = "Welcome to the chateau, sir. Eloise at your service."
            await play_voice_response(guild.id, greeting)

            target_ch = find_target_channel(guild)
            if target_ch and target_ch.permissions_for(guild.me).send_messages:
                await target_ch.send(
                    f"🎙️ **Eloise Connected to Voice:** `{target_vc.name}`.\n"
                    f"*\"Welcome to the chateau, sir. Eloise at your service.\"*\n"
                    f"Say **\"Éloïse\"** or **\"Eloise\"** into your headset mic, or type your questions here in #{target_ch.name} anytime!"
                )
        except Exception as e:
            print(f"[Voice Auto-Join Error]: {e}", flush=True)

        return active_voice_clients.get(guild.id)

# ---------------------------------------------------------------------------
# WATCHDOG LOOP (Guarantees zero idle disconnections)
# ---------------------------------------------------------------------------

@tasks.loop(seconds=12)
async def voice_watchdog_loop():
    """Periodic watchdog that guarantees Eloise stays connected to HUNGER VC and never drops due to idle timeouts."""
    for guild in bot.guilds:
        target_vc = None
        for vc in guild.voice_channels:
            if vc.name.strip().upper() == "HUNGER":
                target_vc = vc
                break
        if not target_vc:
            continue

        humans = [m for m in target_vc.members if not m.bot]
        current_vc = active_voice_clients.get(guild.id)

        # If humans are in HUNGER and Eloise voice client is missing or disconnected
        if humans and (not current_vc or not current_vc.is_connected()):
            print(f"[Watchdog] Humans active in '{target_vc.name}' but Eloise voice dropped. Auto-reconnecting...", flush=True)
            await auto_join_active_voice(guild)

# ---------------------------------------------------------------------------
# LOCAL MIC CALLBACKS (called from background thread — schedule on bot.loop)
# ---------------------------------------------------------------------------

def on_local_voice_heard(raw_text: str):
    """Update the live 'Last Heard from Mic' status line in #hunger ONLY IF connected to HUNGER VC."""
    if not is_eloise_active_in_hunger():
        return

    async def _update():
        for guild in bot.guilds:
            target_ch = find_target_channel(guild)
            if target_ch and target_ch.permissions_for(guild.me).send_messages:
                await safe_update_status(
                    target_ch,
                    f"🎧 **Microphone Entendu :** *\"{raw_text}\"*",
                    "mic"
                )
    asyncio.run_coroutine_threadsafe(_update(), bot.loop)


def on_local_voice_wake(lang: str = "en"):
    """Triggered when user says 'Éloïse' — ONLY active if connected to HUNGER VC."""
    if not is_eloise_active_in_hunger():
        return

    stop_all_speech()  # Instant barge-in: terminate any playing speech in headset and Discord!
    global active_command_window
    active_command_window = time.time() + 8.0  # 8s active window for the question

    spoken = "Oui ?" if lang == "fr" else "Yes ?"
    print(f"\n[Eloise Wake]: \"{spoken}\" (barge-in cutoff, 8s window open)", flush=True)

    # 1. Play immediately in PC headphones
    speak_async(spoken, voice=TTS_VOICE)

    async def _confirm():
        for guild in bot.guilds:
            if guild.id not in active_voice_clients:
                continue
            # Play in Discord voice
            await play_voice_response(guild.id, spoken)
            # Update status in #hunger-helper
            target_ch = find_target_channel(guild)
            if target_ch:
                await safe_update_status(
                    target_ch,
                    f"👂 **Eloise:** *\"{spoken}\"* ⏳ *(8s active — posez votre question)*",
                    "wake"
                )
    asyncio.run_coroutine_threadsafe(_confirm(), bot.loop)


def on_local_voice_command(query: str, lang: str = "en", has_wake: bool = False):
    """Triggered when user gives a command (after wake-word or in active window) — ONLY active if connected to HUNGER VC."""
    if not is_eloise_active_in_hunger():
        return

    global active_command_window

    clean_q = re.sub(r"^[\s,\.?!;:\-]+|[\s,\.?!;:\-]+$", "", query).strip().lower()
    if not clean_q or len(clean_q) < 2:
        return

    # Check for immediate STOP / SILENCE command FIRST (bypasses window check)
    is_stop_cmd = any(w in clean_q for w in [
        "stop", "stoppe", "arrête", "arrete", "arrête-toi", "arrete-toi",
        "tais-toi", "tais toi", "ferme-la", "ferme la", "chut", "shut up", "silence", "pause"
    ])
    if is_stop_cmd:
        stop_all_speech()  # Cut off audio immediately
        active_command_window = 0.0
        # Memory, user profile progression, and raid timers are 100% PRESERVED!
        print(f"[Eloise Emergency Stop]: Voice cut off instantly. Zero speech. Memory and progress preserved.", flush=True)

        async def _notify_stop():
            for guild in bot.guilds:
                target_ch = find_target_channel(guild)
                if target_ch:
                    await safe_update_status(target_ch, "🤫 **Mode Silence Immédiat (Voix coupée - Mémoire 100% Préservée)**", "wake")
        asyncio.run_coroutine_threadsafe(_notify_stop(), bot.loop)
        return

    now = time.time()
    is_in_window = now < active_command_window

    # STRICT RULE: Must have said wake word OR be inside the active window!
    # Prevents triggering on casual chatter with friends in voice channel.
    if not has_wake and not is_in_window:
        return

    stop_all_speech()  # Instant cut-off of any prior speech!
    active_command_window = 0.0  # Reset window immediately
    print(f"\n[Eloise Command]: \"{clean_q}\" (lang={lang}, wake={has_wake})", flush=True)

    # Immediate voice acknowledgment ("Ok")
    ack_spoken = "Ok"
    speak_async(ack_spoken, voice=TTS_VOICE)

    async def _process():
        # Acknowledge in Discord voice
        for guild in bot.guilds:
            if guild.id in active_voice_clients:
                await play_voice_response(guild.id, ack_spoken)

        # Run brain processing in executor so it doesn't block the event loop
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, brain.process_message, "local_player", "Commander", clean_q
        )

        spoken = result.get("spoken_text", "")
        display = result.get("display_text", "")
        img_path = result.get("image_attachment")

        # 1. Speak in PC headphones ONLY if spoken text is non-empty
        if spoken:
            speak_async(spoken, voice=TTS_VOICE)

        # 2. Post to Discord voice + #hunger
        for guild in bot.guilds:
            if guild.id not in active_voice_clients:
                continue

            # Play in voice channel ONLY if spoken text is non-empty
            if spoken:
                await play_voice_response(guild.id, spoken)

            # Post tactical intel to #hunger-helper
            target_ch = find_target_channel(guild)
            if target_ch and display:
                img_paths = result.get("image_attachments") or ([result["image_attachment"]] if result.get("image_attachment") else [])
                files_to_send = [discord.File(p, filename=os.path.basename(p)) for p in img_paths if os.path.exists(p)]

                print(f"[Eloise] Posting to #{target_ch.name}: {display[:60]}...", flush=True)
                try:
                    if files_to_send:
                        await target_ch.send(
                            content=f"⚔️ **Eloise Tactical Intel:**\n{display}",
                            files=files_to_send
                        )
                    else:
                        await target_ch.send(
                            content=f"⚔️ **Eloise Tactical Intel:**\n{display}"
                        )
                except discord.Forbidden:
                    print(f"[Discord Permission Error] Lacking 'Send Messages' or 'Attach Files' in #{target_ch.name}! Please allow permissions for role HUNGER.", flush=True)
                except Exception as e:
                    print(f"[Discord Post Error in #{target_ch.name}]: {e}", flush=True)

    asyncio.run_coroutine_threadsafe(_process(), bot.loop)

# ---------------------------------------------------------------------------
# BOT EVENTS
# ---------------------------------------------------------------------------

@bot.event
async def on_ready():
    print(f"==================================================")
    print(f"  Eloise Tactical Co-Pilot: {bot.user}")
    print(f"  Whisper Large-v3-Turbo | RTX 3070 CUDA | fr-FR Neural TTS")
    print(f"==================================================")

    # Set nickname in all guilds
    for guild in bot.guilds:
        try:
            await guild.me.edit(nick="Eloise")
        except Exception:
            pass

    # Pre-warm common voice phrases for zero-latency instant response
    async def _warmup():
        for phrase in ["Oui ?", "Ok", "Yes ?", "Welcome to the chateau, sir. Eloise at your service."]:
            try:
                await generate_speech_file(phrase, f"cached_{abs(hash(phrase))}.mp3")
            except Exception:
                pass
    asyncio.create_task(_warmup())

    # Start mic listener thread
    def _run_mic():
        global mic_listener_instance
        mic_listener_instance = LocalMicListener(
            on_command=on_local_voice_command,
            on_wake=on_local_voice_wake,
            on_heard=on_local_voice_heard,
            is_active=is_eloise_active_in_hunger
        )
        mic_listener_instance.start()

    threading.Thread(target=_run_mic, daemon=True).start()

    # Auto-join voice channel with players
    for guild in bot.guilds:
        await auto_join_active_voice(guild)

    # Launch watchdog loop to auto-heal voice disconnects
    if not voice_watchdog_loop.is_running():
        voice_watchdog_loop.start()
        print("[Watchdog] Voice auto-reconnect watchdog active (12s interval).", flush=True)

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.", flush=True)
    except Exception as e:
        print(f"[Slash Sync Error]: {e}", flush=True)


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    guild = member.guild
    current_vc = guild.voice_client

    # 1. ELOISE HERSELF WAS MOVED
    if member.id == bot.user.id:
        if after.channel is not None:
            # If moved to ANY channel other than HUNGER -> disconnect & silence immediately
            if after.channel.name.strip().upper() != "HUNGER":
                print(f"[Voice] Eloise moved to '{after.channel.name}' (not HUNGER). Disconnecting & silencing immediately.", flush=True)
                stop_all_speech()
                if current_vc and current_vc.is_connected():
                    await current_vc.disconnect()
                active_voice_clients.pop(guild.id, None)
                target_ch = find_target_channel(guild)
                if target_ch and target_ch.permissions_for(guild.me).send_messages:
                    try:
                        await target_ch.send("💤 **Éloïse :** Déconnectée — Éloïse opère exclusivement dans le salon vocal `HUNGER`.")
                    except Exception:
                        pass
        return

    # Ignore other bots
    if member.bot:
        return

    # Find the HUNGER voice channel in this guild
    hunger_vc = None
    for vc in guild.voice_channels:
        if vc.name.strip().upper() == "HUNGER":
            hunger_vc = vc
            break

    if not hunger_vc:
        return

    # Count humans currently in HUNGER
    humans_in_hunger = [m for m in hunger_vc.members if not m.bot]

    # CASE A: No humans in HUNGER -> Eloise MUST NOT be in voice channel
    if not humans_in_hunger:
        if current_vc and current_vc.is_connected():
            print(f"[Voice] No players in HUNGER. Eloise leaving and silencing.", flush=True)
            stop_all_speech()
            await current_vc.disconnect()
            active_voice_clients.pop(guild.id, None)
            target_ch = find_target_channel(guild)
            if target_ch and target_ch.permissions_for(guild.me).send_messages:
                try:
                    await target_ch.send("💤 **Éloïse :** Déconnectée du vocal — aucun joueur dans `HUNGER`. En veille silencieuse.")
                except Exception:
                    pass
        return

    # CASE B: Humans ARE in HUNGER!
    # If Eloise is not connected, or connected to another channel, connect strictly to HUNGER
    if not current_vc or not current_vc.is_connected():
        await auto_join_active_voice(guild)
    elif current_vc.channel.id != hunger_vc.id:
        await current_vc.move_to(hunger_vc)
        active_voice_clients[guild.id] = current_vc
    elif after.channel and after.channel.id == hunger_vc.id and before.channel != after.channel:
        # A human just entered HUNGER while Eloise is in it
        await asyncio.sleep(1.0)
        greeting = "Welcome to the chateau, sir. Eloise at your service."
        await play_voice_response(guild.id, greeting)
        speak_async(greeting, voice=TTS_VOICE)
        target_ch = find_target_channel(guild)
        if target_ch and target_ch.permissions_for(guild.me).send_messages:
            try:
                await target_ch.send(f"👋 **Éloïse :** Bienvenue à **{member.display_name}** dans le vocal `HUNGER`.")
            except Exception:
                pass


# ---------------------------------------------------------------------------
# SLASH COMMANDS
# ---------------------------------------------------------------------------

@bot.tree.command(name="join", description="Connecter Éloïse au salon vocal HUNGER")
async def join(interaction: discord.Interaction):
    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("❌ Vous devez être dans le salon vocal **HUNGER** !", ephemeral=True)
        return
    v_channel = interaction.user.voice.channel
    if v_channel.name.strip().upper() != "HUNGER":
        await interaction.response.send_message("❌ Éloïse opère exclusivement dans le salon vocal **HUNGER**.", ephemeral=True)
        return
    guild_id = interaction.guild_id
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.move_to(v_channel)
        vc = interaction.guild.voice_client
    else:
        vc = await v_channel.connect()
    active_voice_clients[guild_id] = vc
    greeting = "Welcome to the chateau, sir. Eloise at your service."
    await interaction.response.send_message(f"🎙️ Éloïse connectée au salon vocal **{v_channel.name}**.")
    await play_voice_response(guild_id, greeting)
    speak_async(greeting, voice=TTS_VOICE)
    greeting = "Welcome to the chateau, sir. Eloise at your service."
    await interaction.response.send_message(f"🎙️ Eloise connected to **{v_channel.name}**.")
    await play_voice_response(guild_id, greeting)
    speak_async(greeting, voice=TTS_VOICE)


@bot.tree.command(name="leave", description="Disconnect Eloise from voice")
async def leave(interaction: discord.Interaction):
    guild_id = interaction.guild_id
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        active_voice_clients.pop(guild_id, None)
        await interaction.response.send_message("👋 Eloise disconnected from voice channel.")
    else:
        await interaction.response.send_message("I am not in a voice channel.", ephemeral=True)


@bot.tree.command(name="ask", description="Ask Eloise a question or give a command")
@app_commands.describe(query="Your question or command")
async def ask(interaction: discord.Interaction, query: str):
    await interaction.response.defer()
    user_id = str(interaction.user.id)
    username = interaction.user.display_name
    result = brain.process_message(user_id, username, query)

    spoken = result.get("spoken_text", "")
    display = result.get("display_text", "")
    img_path = result.get("image_attachment")

    if spoken and interaction.guild_id in active_voice_clients:
        await play_voice_response(interaction.guild_id, spoken)
        speak_async(spoken, voice=TTS_VOICE)

    img_paths = result.get("image_attachments") or ([result["image_attachment"]] if result.get("image_attachment") else [])
    files_to_send = [discord.File(p, filename=os.path.basename(p)) for p in img_paths if os.path.exists(p)]

    if files_to_send:
        await interaction.followup.send(content=display or spoken, files=files_to_send)
    else:
        await interaction.followup.send(content=display or spoken)


@bot.tree.command(name="map", description="Generate a tactical raid map")
@app_commands.describe(map_name="Sarlat Farm, Sombre Forest, or Jacques Bridge")
async def raid_map(interaction: discord.Interaction, map_name: str = "Sarlat Farm"):
    await interaction.response.defer()
    user_id = str(interaction.user.id)
    username = interaction.user.display_name
    result = brain.process_message(user_id, username, f"post map {map_name}")

    spoken = result.get("spoken_text", "")
    display = result.get("display_text", "")
    img_path = result.get("image_attachment")

    if spoken and interaction.guild_id in active_voice_clients:
        await play_voice_response(interaction.guild_id, spoken)
        speak_async(spoken, voice=TTS_VOICE)

    file_to_send = None
    if img_path and os.path.exists(img_path):
        file_to_send = discord.File(img_path, filename="tactical_map.jpg")

    await interaction.followup.send(content=display or spoken, file=file_to_send)

    # Also post to #hunger-helper if command came from elsewhere
    target_ch = find_target_channel(interaction.guild)
    if file_to_send and target_ch and target_ch.id != interaction.channel_id:
        try:
            map_file2 = discord.File(img_path, filename="tactical_map.jpg")
            await target_ch.send(content=f"🗺️ **Raid Intel Map: {map_name.title()}:**", file=map_file2)
        except Exception:
            pass

    # Pre-warm common voice phrases for zero-latency instant response
    async def _warmup():
        for phrase in ["Oui ?", "Ok", "Yes ?", "Welcome to the chateau, sir. Eloise at your service."]:
            try:
                await generate_speech_file(phrase, f"cached_{abs(hash(phrase))}.mp3")
            except Exception:
                pass
    asyncio.create_task(_warmup())


@bot.tree.command(name="config-gemini", description="Configure your free Google Gemini API key for automated screenshot stash & inventory vision")
@app_commands.describe(key="Your Google AI Studio Gemini API key (from https://aistudio.google.com)")
async def config_gemini(interaction: discord.Interaction, key: str):
    from co_pilot.vision_analyzer import set_gemini_api_key
    ok = set_gemini_api_key(key)
    if ok:
        await interaction.response.send_message(
            content="✅ **Clé Gemini API configurée avec succès !**\n"
                    "Éloïse peut désormais scanner instantanément vos captures d'écran d'inventaire, de sac de raid et de coffre de stash avec l'IA Vision !\n"
                    "📸 *Uploadez simplement un screenshot dans ce salon avec votre question.*",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            content="⚠️ **Erreur lors de l'enregistrement de la clé.**",
            ephemeral=True
        )

@bot.tree.command(name="progress", description="Check your quest and progression summary")
async def progress(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    target = member or interaction.user
    user_id = str(target.id)
    summary = get_user_progression_summary(user_id)

    embed = discord.Embed(
        title=f"📊 Combat Record: {target.display_name}",
        description=f"**Level:** {summary['level']} | **Completed Quests:** {summary['completed_count']}",
        color=0xE67E22
    )
    if summary["active_quests"]:
        q_list = "\n".join([f"• **{q['name']}** ({q.get('location', 'World')})" for q in summary["active_quests"]])
        embed.add_field(name="🎯 Active Quests", value=q_list, inline=False)
    else:
        embed.add_field(name="🎯 Active Quests", value="*No quests currently active.*", inline=False)
    if summary.get("available_quests"):
        avail_list = "\n".join([f"• **{q['name']}** (from {q['giver']})" for q in summary["available_quests"][:5]])
        embed.add_field(name="📋 Next Available", value=avail_list, inline=False)
    if summary.get("talents"):
        t_list = "\n".join([f"• **{t['name']}**: {t['allocated_points']}/{t['max_points']} ({t['mastery_name']})" for t in summary["talents"]])
        embed.add_field(name="⚡ Talents", value=t_list, inline=False)
    await interaction.response.send_message(embed=embed)


# ---------------------------------------------------------------------------
# INTERACTIVE MAP & ITEM QUICK-VIEWS (Buttons attached to Discord Images)
# ---------------------------------------------------------------------------

@bot.tree.command(name="eloise", description="Ask Eloise any tactical question about The Hunger (weapons, HTK, loot, maps, drops, lore)")
@app_commands.describe(question="Your tactical question (e.g. 'where is farmer dreg', 'show me dagger skins', 'borodino htk')")
async def eloise_cmd(interaction: discord.Interaction, question: str):
    await interaction.response.defer()
    user_id = str(interaction.user.id)
    username = interaction.user.display_name
    res = brain.process_message(user_id, username, question)
    display = res.get("display_text") or res.get("spoken_text", "")
    img_paths = res.get("image_attachments") or ([res["image_attachment"]] if res.get("image_attachment") else [])
    files_to_send = [discord.File(p, filename=os.path.basename(p)) for p in img_paths if os.path.exists(p)]
    if files_to_send:
        await interaction.followup.send(content=f"{interaction.user.mention} ⚔️ **Eloise :**\n{display}", files=files_to_send)
    else:
        await interaction.followup.send(content=f"{interaction.user.mention} ⚔️ **Eloise :**\n{display}")


class TacticalMapQuickView(discord.ui.View):
    def __init__(self, target_map: str = "Sarlat Farm"):
        super().__init__(timeout=300.0)
        self.target_map = target_map

    @discord.ui.button(label="🏰 Donjon & Entrées", style=discord.ButtonStyle.primary, emoji="🏰")
    async def dungeon_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        res = brain.process_message(str(interaction.user.id), interaction.user.display_name, f"carte donjon {self.target_map}")
        img = res.get("image_attachment")
        f = discord.File(img, filename=os.path.basename(img)) if img and os.path.exists(img) else None
        await interaction.followup.send(content=f"{interaction.user.mention} 🏰 **Donjon ({self.target_map}) :**\n{res.get('display_text')}", file=f)

    @discord.ui.button(label="👾 Baveux & Brutes", style=discord.ButtonStyle.danger, emoji="👾")
    async def creatures_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        res = brain.process_message(str(interaction.user.id), interaction.user.display_name, f"map baveux brute {self.target_map}")
        img = res.get("image_attachment")
        f = discord.File(img, filename=os.path.basename(img)) if img and os.path.exists(img) else None
        await interaction.followup.send(content=f"{interaction.user.mention} 👾 **Créatures & Équarrissage :**\n{res.get('display_text')}", file=f)

    @discord.ui.button(label="🚪 Extractions", style=discord.ButtonStyle.secondary, emoji="🚪")
    async def extract_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        res = brain.process_message(str(interaction.user.id), interaction.user.display_name, f"extractions {self.target_map}")
        await interaction.followup.send(content=f"{interaction.user.mention} 🚪 **Points d'Extraction :**\n{res.get('display_text')}")

    @discord.ui.button(label="⏱️ Temps Écoulé de Raid", style=discord.ButtonStyle.success, emoji="⏱️")
    async def chrono_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        res = brain.process_message(str(interaction.user.id), interaction.user.display_name, "combien de temps est passé")
        await interaction.followup.send(content=f"{interaction.user.mention} ⏱️ **Chronomètre de Raid :**\n{res.get('display_text')}")


class ItemCardQuickView(discord.ui.View):
    def __init__(self, item_name: str = "item"):
        super().__init__(timeout=300.0)
        self.item_name = item_name

    @discord.ui.button(label="🎒 Utile pour mes Quêtes ?", style=discord.ButtonStyle.primary, emoji="🎒")
    async def quest_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        res = brain.process_message(str(interaction.user.id), interaction.user.display_name, f"est-ce que j'ai besoin de {self.item_name}")
        await interaction.followup.send(content=f"{interaction.user.mention} 🎒 **Analyse Quête ({self.item_name.title()}) :**\n{res.get('display_text')}")

    @discord.ui.button(label="⚔️ Simulateur TTK", style=discord.ButtonStyle.danger, emoji="⚔️")
    async def ttk_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        res = brain.process_message(str(interaction.user.id), interaction.user.display_name, f"combien de coups avec {self.item_name} pour tuer la brute")
        await interaction.followup.send(content=f"{interaction.user.mention} ⚔️ **Simulateur de Combat ({self.item_name.title()}) :**\n{res.get('display_text')}")

    @discord.ui.button(label="🛒 Vendeur au Château", style=discord.ButtonStyle.secondary, emoji="🛒")
    async def vendor_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        res = brain.process_message(str(interaction.user.id), interaction.user.display_name, f"quel marchand vend {self.item_name}")
        await interaction.followup.send(content=f"{interaction.user.mention} 🛒 **Disponibilité Marchand ({self.item_name.title()}) :**\n{res.get('display_text')}")




class QuestCardQuickView(discord.ui.View):
    def __init__(self, quest_name: str = "quête"):
        super().__init__(timeout=300.0)
        self.quest_name = quest_name

    @discord.ui.button(label="🗺️ Carte & Emplacement", style=discord.ButtonStyle.primary, emoji="🗺️")
    async def map_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        res = brain.process_message(str(interaction.user.id), interaction.user.display_name, f"ou se trouve {self.quest_name}")
        img = res.get("image_attachment")
        f = discord.File(img, filename=os.path.basename(img)) if img and os.path.exists(img) else None
        await interaction.followup.send(content=f"{interaction.user.mention} 🗺️ **Carte Tactique ({self.quest_name.title()}) :**\n{res.get('display_text')}", file=f)

    @discord.ui.button(label="🎒 Items Requis en Raid", style=discord.ButtonStyle.success, emoji="🎒")
    async def items_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        res = brain.process_message(str(interaction.user.id), interaction.user.display_name, f"est-ce que j'ai besoin d'un item pour {self.quest_name}")
        await interaction.followup.send(content=f"{interaction.user.mention} 🎒 **Items Requis :**\n{res.get('display_text')}")

    @discord.ui.button(label="📜 Quêtes Suivantes", style=discord.ButtonStyle.secondary, emoji="📜")
    async def next_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        res = brain.process_message(str(interaction.user.id), interaction.user.display_name, "quelles sont mes prochaines quêtes")
        await interaction.followup.send(content=f"{interaction.user.mention} 📜 **Suite de la Progression :**\n{res.get('display_text')}")

# ---------------------------------------------------------------------------
# TEXT CHAT LISTENER (typing commands in #hunger)
# ---------------------------------------------------------------------------

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    content_raw = message.content.strip()
    content_lower = content_raw.lower()

    is_dm = message.guild is None
    ch_name = message.channel.name.lower().replace("-", "").replace("_", "") if not is_dm else "dm"
    
    # Dedicated channels: #hunger, #hunger-helper, #eloise, #the-hunger, #bot
    is_dedicated = is_dm or any(k in ch_name for k in ["hunger", "eloise", "thehunger", "companion", "bot"])
    is_mentioned = (bot.user in message.mentions) or any(
        content_lower.startswith(w) for w in WAKE_WORDS
    ) or content_lower.startswith("!eloise") or content_lower.startswith("?eloise")

    should_process = is_dedicated or is_mentioned

    # 0. SCREENSHOT INVENTORY / STASH VISION SCANNER
    if should_process and message.attachments:
        img_att = None
        for att in message.attachments:
            if att.content_type and any(t in att.content_type.lower() for t in ["image", "png", "jpeg", "jpg", "webp"]):
                img_att = att
                break
            elif any(att.filename.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp"]):
                img_att = att
                break

        if img_att:
            temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "temp_audio"))
            os.makedirs(temp_dir, exist_ok=True)
            save_path = os.path.join(temp_dir, f"screen_{message.author.id}_{int(time.time()*1000)}.png")
            await img_att.save(save_path)

            from co_pilot.vision_analyzer import analyze_inventory_screenshot
            status_wait = await message.reply("🔍 **Analyse visuelle de votre inventaire en cours avec l'IA Vision...**")

            res_vis = await analyze_inventory_screenshot(
                save_path, message.clean_content, str(message.author.id), message.author.display_name
            )

            spoken = res_vis.get("spoken_text", "")
            display = res_vis.get("display_text", "")
            img_paths = res_vis.get("image_attachments") or ([res_vis["image_attachment"]] if res_vis.get("image_attachment") else [])

            if spoken and message.guild and message.guild.id in active_voice_clients:
                await play_voice_response(message.guild.id, spoken)

            files_to_send = [discord.File(p, filename=os.path.basename(p)) for p in img_paths if os.path.exists(p)]

            try:
                await status_wait.delete()
            except Exception:
                pass

            dest = message.channel
            if files_to_send:
                await dest.send(content=f"{message.author.mention} ⚔️ **Eloise :**\n{display}", files=files_to_send)
            else:
                await dest.send(content=f"{message.author.mention} ⚔️ **Eloise :**\n{display}")
            return

    # 0.1 TEXT INVENTORY / STASH APPRAISER ("j'ai 3 farines, 1 deux, combien ca vaut")
    if should_process and any(w in content_lower for w in ["j'ai", "jai", "combien vaut mon", "combien valent mes", "combien vaut mon sac", "combien vaut mon inventaire"]) and any(w in content_lower for w in ["farine", "deux", "salpetre", "salpêtre", "bague", "charbon", "cle", "clé", "sacs"]):
        from co_pilot.vision_analyzer import appraise_text_inventory
        appraise_res = appraise_text_inventory(content_raw, is_french=True)
        spoken = appraise_res.get("spoken_text", "")
        display = appraise_res.get("display_text", "")
        if spoken and message.guild and message.guild.id in active_voice_clients:
            await play_voice_response(message.guild.id, spoken)
        await message.reply(content=f"{message.author.mention} ⚔️ **Eloise :**\n{display}")
        return

    # 1. TEXT COMMAND: !reconnect / !restart / !relancer (server only)
    if should_process and message.guild and content_lower in ["!reconnect", "!restart", "!relancer", "!rejoin", "!join", "!reset"]:
        status_msg = await message.channel.send("🔄 **Réinitialisation en cours...** Reconnexion au salon vocal et recalibrage du micro casque...")
        stop_all_speech()
        await auto_join_active_voice(message.guild)
        new_gate = 220.0
        if mic_listener_instance:
            new_gate = mic_listener_instance.recalibrate(duration=0.8)

        is_connected = is_eloise_active_in_hunger()
        vc_desc = "Connectée ✅ (Salon HUNGER)" if is_connected else "En attente ⚠️ (Rejoignez le salon vocal HUNGER)"
        await status_msg.edit(
            content=(
                f"✅ **Éloïse est opérationnelle !**\n"
                f"• 🎙️ **Salon Vocal :** `{vc_desc}`\n"
                f"• 🎧 **Micro Casque HyperX :** Recalibré (Seuil de détection : `{new_gate:.1f}` RMS)\n"
                f"• 💬 **Mode Écrit :** Vous et vos coéquipiers pouvez poser vos questions directement ici !"
            )
        )
        if is_connected:
            await play_voice_response(message.guild.id, "De retour, monsieur. Éloïse à votre service.")
        return

    # 2. TEXT COMMAND: !status / !statut / !ping
    if should_process and content_lower in ["!status", "!statut", "!ping"]:
        st = mic_listener_instance.get_status() if mic_listener_instance else {}
        is_connected = is_eloise_active_in_hunger() if message.guild else False
        await message.channel.send(
            f"🛡️ **STATUT TACTIQUE D'ÉLOÏSE :**\n"
            f"• 🎙️ **Vocal HUNGER :** {'Connectée et active ✅' if is_connected else 'Inactif (Mode Écrit disponible partout) 💬'}\n"
            f"• 🧠 **IA Moteur :** Faster-Whisper Large-v3-Turbo (RTX 3070 CUDA fp16)\n"
            f"• 🔊 **Synthèse Vocale :** Edge-TTS fr-FR-Vivienne Multilingual Neural\n"
            f"• 🌐 **Serveurs Connectés :** `{len(bot.guilds)}` | **Accès :** Sans restriction dans tous les salons !"
        )
        return

    # 3. TEXT COMMAND: !help / !aide
    if should_process and content_lower in ["!help", "!aide"]:
        await message.channel.send(
            f"📖 **GUIDE D'UTILISATION D'ÉLOÏSE :**\n\n"
            f"💬 **Par Écrit (Sur n'importe quel Discord & en Message Privé) :**\n"
            f"• Posez directement votre question dans un salon `#hunger` ou `#eloise` !\n"
            f"• Dans les autres salons, mentionnez simplement **@Eloise** ou commencez par **eloise** !\n"
            f"• Vous pouvez aussi utiliser la commande slash universelle **/eloise** !\n\n"
            f"🔍 **Exemples de questions tactiques :**\n"
            f"• `show me dagger skins` (toutes les cartes cosmétiques)\n"
            f"• `where can i find farmer dreg` (carte tactique de spawn et loot 100%)\n"
            f"• `show me a map with all the brute and drooler spawns` (carte complète 20 points)\n"
            f"• `combien de coups avec un borodino pour tuer du violet` (simulateur HTK)\n"
            f"• `recette brioche` ou `schema sapper cuirass` (recettes et composants)\n"
            f"• `donjon the pit` ou `carte donjon jacques folly` (cartes souterraines)"
        )
        return

    # 4. GENERAL QUESTIONS (FROM YOU OR ANY SQUADMATE ON ANY SERVER!)
    if should_process:
        cleaned = message.clean_content
        # Strip bot mention and wake words
        cleaned = re.sub(r"@" + re.escape(bot.user.name), "", cleaned, flags=re.IGNORECASE)
        for w in WAKE_WORDS + ["!eloise", "?eloise"]:
            cleaned = re.sub(r"^\b" + re.escape(w) + r"\b[\s,;:\?!-]*", "", cleaned, flags=re.IGNORECASE)
        cleaned = cleaned.strip()

        if not cleaned:
            await message.reply("À votre service. Posez votre question tactique ou utilisez `/eloise` !")
            await bot.process_commands(message)
            return

        user_id = str(message.author.id)
        username = message.author.display_name
        result = brain.process_message(user_id, username, cleaned)

        spoken = result.get("spoken_text", "")
        display = result.get("display_text", "")
        img_path = result.get("image_attachment")

        # Play spoken tactical audio in Discord voice ONLY if that guild has active voice
        if spoken and message.guild and message.guild.id in active_voice_clients:
            await play_voice_response(message.guild.id, spoken)

        img_paths = result.get("image_attachments") or ([result["image_attachment"]] if result.get("image_attachment") else [])
        files_to_send = [discord.File(p, filename=os.path.basename(p)) for p in img_paths if os.path.exists(p)]

        dest = message.channel
        if files_to_send:
            await dest.send(
                content=f"{message.author.mention} ⚔️ **Eloise :**\n{display or spoken}",
                files=files_to_send
            )
        else:
            await dest.send(
                content=f"{message.author.mention} ⚔️ **Eloise :**\n{display or spoken}"
            )

    await bot.process_commands(message)

# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

def run():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

    # Prevent multiple bot instances (causes Discord 4006 voice errors)
    import socket
    _lock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        _lock.bind(("127.0.0.1", 49152))
        _lock.listen(1)
    except socket.error:
        print("\n[WARNING] Eloise is already running! Close the existing window first.\n")
        return

    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config.json"))
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    token = cfg.get("DISCORD_BOT_TOKEN")
            except Exception:
                pass

    if not token or token == "YOUR_DISCORD_BOT_TOKEN_HERE":
        print("\n[Error] DISCORD_BOT_TOKEN not set.")
        return

    bot.run(token)


if __name__ == "__main__":
    run()
