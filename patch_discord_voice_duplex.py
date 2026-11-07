import os, re

p = "co_pilot/discord_bot.py"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Imports and Opus loading
target_imports = """from co_pilot.mic_listener import LocalMicListener"""
replace_imports = """from co_pilot.mic_listener import LocalMicListener
from discord.ext import voice_recv
from co_pilot.discord_voice_listener import DiscordSquadVoiceSink

# Ensure Opus library is loaded for Discord voice transmit/receive
if not discord.opus.is_loaded():
    discord.opus._load_default()
    print(f"[Discord Voice Core] Opus encoder loaded: {discord.opus.is_loaded()}", flush=True)"""

assert target_imports in text, "target_imports not found"
text = text.replace(target_imports, replace_imports, 1)

# 2. Active sinks dictionary and locks
target_state = """# Active voice client per guild
active_voice_clients: Dict[int, discord.VoiceClient] = {}
# Global reference to live mic listener instance
mic_listener_instance: Optional[LocalMicListener] = None"""

replace_state = """# Active voice client per guild
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
    return _guild_voice_locks[guild_id]"""

assert target_state in text, "target_state not found"
text = text.replace(target_state, replace_state, 1)

# 3. Speech WAV synthesis & LOUD play_voice_response
target_speech = """_TTS_CACHE: Dict[str, str] = {}

async def generate_speech_file(text: str, filename: str = "copilot_speech.mp3") -> str:
    \"\"\"Generate audio file using Edge-TTS with natural French-accented voice, using disk caching for speed.\"\"\"
    temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "temp_audio"))
    os.makedirs(temp_dir, exist_ok=True)

    cache_key = f"{TTS_VOICE}_{text.strip().lower()}"
    if cache_key in _TTS_CACHE and os.path.exists(_TTS_CACHE[cache_key]):
        return _TTS_CACHE[cache_key]

    out_path = os.path.join(temp_dir, filename)
    comm = edge_tts.Communicate(text, TTS_VOICE)
    await comm.save(out_path)
    _TTS_CACHE[cache_key] = out_path
    return out_path

async def play_voice_response(guild_id: int, text: str):
    \"\"\"Play spoken response in the connected voice channel.\"\"\"
    if not text or not text.strip():
        return
    vc = active_voice_clients.get(guild_id)
    if not vc or not vc.is_connected():
        return
    # Clean markdown and special symbols so Edge-TTS never fails
    clean = re.sub(r"[\*#_~`\|]+", " ", text)
    clean = re.sub(r"[^\w\s\.,\?!'-]", " ", clean).strip()
    clean = re.sub(r"\s+", " ", clean).strip()
    if not clean or len(clean) < 1:
        return
    try:
        unique_name = f"speech_{guild_id}_{int(time.time() * 1000)}.mp3"
        audio_file = await generate_speech_file(clean, unique_name)
        if not audio_file or not os.path.exists(audio_file):
            return

        # Wait gracefully if already playing (e.g. short 'Ok' or 'Oui ?')
        attempts = 0
        while vc.is_playing() and attempts < 15:
            await asyncio.sleep(0.1)
            attempts += 1
        if vc.is_playing():
            vc.stop()
            await asyncio.sleep(0.05)

        audio_source = discord.FFmpegPCMAudio(
            executable=FFMPEG_EXE,
            source=audio_file,
            options="-vn"
        )
        vc.play(audio_source)
        print(f"[Eloise Discord Voice]: \\\"{clean}\\\"", flush=True)
    except Exception as e:
        print(f"[Voice Output Error]: {e}", flush=True)"""

replace_speech = """_TTS_CACHE: Dict[str, str] = {}

async def generate_speech_wav(text: str, filename_prefix: str = "copilot_speech") -> str:
    \"\"\"Synthesize audio and convert directly to clean 48kHz 16-bit stereo PCM WAV for zero-distortion Discord playback.\"\"\"
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
    \"\"\"Play loud, clear spoken response in the connected Discord voice channel without cutting off.\"\"\"
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
            print(f"[Eloise Discord Voice (LOUD)]: \\\"{clean}\\\"", flush=True)

            while vc.is_playing():
                await asyncio.sleep(0.05)

    except Exception as e:
        print(f"[Voice Output Error]: {e}", flush=True)"""

assert target_speech in text, "target_speech not found"
text = text.replace(target_speech, replace_speech, 1)

# 4. Connect with VoiceRecvClient and attach squad voice listener
target_connect = """            vc = await target_vc.connect(reconnect=True, timeout=12.0)
            active_voice_clients[guild.id] = vc
            print(f"[Voice] Eloise connected to: {target_vc.name}", flush=True)

            await asyncio.sleep(1.0)
            greeting = "Welcome to the chateau, sir. Eloise at your service."
            await play_voice_response(guild.id, greeting)
            speak_async(greeting, voice=TTS_VOICE)"""

replace_connect = """            # Connect using full-duplex VoiceRecvClient to hear squadmates and speak simultaneously!
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
            await play_voice_response(guild.id, greeting)"""

assert target_connect in text, "target_connect not found"
text = text.replace(target_connect, replace_connect, 1)

# 5. Define post_squad_intel_to_chat
target_disconnect = """            if current_vc and current_vc.is_connected():
            ch_name = current_vc.channel.name
            await current_vc.disconnect()
            active_voice_clients.pop(guild.id, None)
            print(f"[Voice] Nobody in HUNGER. Eloise disconnected from: {ch_name}", flush=True)"""

# Find place to add post_squad_intel_to_chat before auto_join_active_voice
target_pre_autojoin = """async def auto_join_active_voice(guild: discord.Guild) -> Optional[discord.VoiceClient]:"""

replace_pre_autojoin = """async def post_squad_intel_to_chat(guild: discord.Guild, uid: int, username: str, display: str, img_path: Optional[str]):
    \"\"\"Post rich tactical card & display response to #hunger tagging the squadmate who asked.\"\"\"
    target_ch = find_target_channel(guild)
    if not target_ch:
        return

    content = f"<@{uid}> ⚔️ **Eloise :**\\n{display}" if display else f"<@{uid}>"
    file_to_send = None
    if img_path and os.path.exists(img_path):
        file_to_send = discord.File(img_path)

    view = None
    if img_path:
        low_p = os.path.basename(img_path).lower()
        if "map" in low_p:
            view = TacticalMapQuickView(os.path.basename(img_path))
        elif "quest" in low_p:
            view = QuestCardQuickView()
        elif "item" in low_p or "weapon" in low_p or "creature" in low_p:
            view = ItemCardQuickView()

    try:
        if file_to_send and view:
            await target_ch.send(content=content, file=file_to_send, view=view)
        elif file_to_send:
            await target_ch.send(content=content, file=file_to_send)
        else:
            await target_ch.send(content=content)
    except Exception as e:
        print(f"[Post Intel Error in #{target_ch.name}]: {e}", flush=True)

async def auto_join_active_voice(guild: discord.Guild) -> Optional[discord.VoiceClient]:"""

assert target_pre_autojoin in text, "target_pre_autojoin not found"
text = text.replace(target_pre_autojoin, replace_pre_autojoin, 1)

# Write out modified file
with open(p, "w", encoding="utf-8") as f:
    f.write(text)

print("co_pilot/discord_bot.py patched with Full-Duplex Multi-User Voice & LOUD Audio Output!")
