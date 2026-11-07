"""
Discord Voice Stream Receiver & Multi-User Squad Listener
Enables Eloise to hear everyone in the HUNGER voice channel in real-time,
transcribe their speech using Faster-Whisper on GPU, and reply directly in Discord voice.
"""

import os
import re
import time
import queue
import threading
import asyncio
import numpy as np
from typing import Dict, List, Optional
import discord
from discord.ext import voice_recv

from co_pilot.mic_listener import whisper_model, WAKE_REGEX, STOP_REGEX

# Ensure Opus is loaded
if not discord.opus.is_loaded():
    discord.opus._load_default()

class DiscordSquadVoiceSink(voice_recv.AudioSink):
    """
    AudioSink attached to VoiceRecvClient.
    Captures live incoming PCM from all squadmates in the voice channel,
    detects speech boundaries per-user, and dispatches to Faster-Whisper.
    """
    def __init__(self, bot: discord.Client, guild: discord.Guild, brain, play_voice_fn, post_intel_fn):
        super().__init__()
        self.bot = bot
        self.guild = guild
        self.brain = brain
        self.play_voice_fn = play_voice_fn
        self.post_intel_fn = post_intel_fn

        # Per-user audio state
        self.buffers: Dict[int, List[np.ndarray]] = {}
        self.last_speech_time: Dict[int, float] = {}
        self.is_speaking: Dict[int, bool] = {}
        self.user_names: Dict[int, str] = {}
        self.user_windows: Dict[int, float] = {}  # 8s active window after saying "Eloise"

        self._lock = threading.Lock()
        self._running = True
        self._worker_thread = threading.Thread(target=self._silence_checker_loop, daemon=True)
        self._worker_thread.start()
        print(f"[Discord Voice Listener] Active for guild '{guild.name}' — Listening to all squadmates in VC.", flush=True)

    def wants_opus(self) -> bool:
        # Request decoded 48kHz 16-bit stereo PCM
        return False

    def write(self, user: Optional[discord.User], data: voice_recv.VoiceData) -> None:
        if user is None or user.bot or not data.pcm:
            return

        uid = user.id
        self.user_names[uid] = user.display_name

        try:
            # 48000Hz 16-bit stereo PCM -> 3840 bytes per 20ms frame
            arr = np.frombuffer(data.pcm, dtype=np.int16).reshape(-1, 2)
            mono = arr.mean(axis=1)
            rms = float(np.sqrt(np.mean(mono ** 2)))
            now = time.time()

            # Downsample 48kHz to 16kHz by taking every 3rd sample (exact 3:1 integer decimation)
            downsampled = (mono[::3] / 32768.0).astype(np.float32)

            with self._lock:
                # Speech energy gate threshold (220.0)
                if rms > 220.0:
                    if uid not in self.buffers:
                        self.buffers[uid] = []
                    self.buffers[uid].append(downsampled)
                    self.last_speech_time[uid] = now
                    self.is_speaking[uid] = True
                elif self.is_speaking.get(uid, False):
                    # In speaking session, add brief trailing frames up to 0.4s to avoid clipping words
                    if now - self.last_speech_time.get(uid, 0) < 0.4:
                        self.buffers[uid].append(downsampled)
        except Exception:
            pass

    def _silence_checker_loop(self):
        while self._running:
            time.sleep(0.06)
            now = time.time()
            finished_utterances = []

            with self._lock:
                for uid, speaking in list(self.is_speaking.items()):
                    if speaking and (now - self.last_speech_time.get(uid, 0) > 0.75):
                        # 750ms of silence after speaking -> sentence complete!
                        chunks = self.buffers.get(uid, [])
                        username = self.user_names.get(uid, "Squadmate")
                        self.buffers[uid] = []
                        self.is_speaking[uid] = False
                        if chunks:
                            audio_arr = np.concatenate(chunks)
                            finished_utterances.append((uid, username, audio_arr))

            for uid, username, audio_arr in finished_utterances:
                # Minimum 0.5s of audio to be valid speech
                if len(audio_arr) >= 16000 * 0.5:
                    threading.Thread(
                        target=self._process_utterance,
                        args=(uid, username, audio_arr),
                        daemon=True
                    ).start()

    def _process_utterance(self, uid: int, username: str, audio_arr: np.ndarray):
        if whisper_model is None:
            return

        try:
            # 1. Transcribe with Faster-Whisper on GPU
            segments, info = whisper_model.transcribe(
                audio_arr,
                language="fr",
                beam_size=1,
                vad_filter=True
            )
            raw_text = " ".join(s.text for s in segments).strip()
            if not raw_text or len(raw_text) < 2:
                return

            print(f"[Discord Voice Heard from {username}]: \"{raw_text}\"", flush=True)

            # 2. Check for Barge-in / Stop commands
            if STOP_REGEX.search(raw_text):
                print(f"[Barge-in Stop by {username}] Silencing immediately.", flush=True)
                asyncio.run_coroutine_threadsafe(
                    self._handle_stop(), self.bot.loop
                )
                return

            # 3. Check for Wake Word or active window
            now = time.time()
            has_wake = bool(WAKE_REGEX.search(raw_text))
            in_window = (now < self.user_windows.get(uid, 0))

            if not has_wake and not in_window:
                # Not addressed to Eloise
                return

            # Clean wake words from query
            clean_q = WAKE_REGEX.sub("", raw_text).strip()
            clean_q = re.sub(r"^[,\.\?\!\s]+", "", clean_q).strip()

            if not clean_q or len(clean_q) < 2:
                # User just called her name: "Éloïse"
                self.user_windows[uid] = now + 8.0  # Open 8s window
                ack_spoken = "Oui ?"
                print(f"[Eloise Discord]: \"{ack_spoken}\" to {username} (8s window open)", flush=True)
                asyncio.run_coroutine_threadsafe(
                    self.play_voice_fn(self.guild.id, ack_spoken), self.bot.loop
                )
                return

            # 4. User asked a complete question!
            self.user_windows[uid] = 0  # Close window
            asyncio.run_coroutine_threadsafe(
                self._dispatch_squad_query(uid, username, clean_q), self.bot.loop
            )
        except Exception as e:
            print(f"[Discord Utterance Processing Error]: {e}", flush=True)

    async def _handle_stop(self):
        vc = self.guild.voice_client
        if vc and vc.is_connected() and vc.is_playing():
            vc.stop()

    async def _dispatch_squad_query(self, uid: int, username: str, clean_q: str):
        # Immediate short verbal ack in Discord voice
        await self.play_voice_fn(self.guild.id, "Reçu, je regarde.")

        # Process in brain executor
        loop = asyncio.get_running_loop()
        res = await loop.run_in_executor(
            None, self.brain.process_message, str(uid), username, clean_q
        )

        spoken = res.get("spoken_text", "")
        display = res.get("display_text", "")
        img_path = res.get("image_attachment")

        # 1. Play spoken answer in Discord vocal channel for whole squad!
        if spoken:
            await self.play_voice_fn(self.guild.id, spoken)

        # 2. Post visual card & text into #hunger
        if self.post_intel_fn:
            await self.post_intel_fn(self.guild, uid, username, display, img_path)

    def cleanup(self):
        self._running = False
        print(f"[Discord Voice Listener] Cleaned up for guild '{self.guild.name}'.", flush=True)
