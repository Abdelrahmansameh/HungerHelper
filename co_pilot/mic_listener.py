import os
import sys
import time
import re
import queue
import threading
import io
import wave
import numpy as np
import sounddevice as sd
import speech_recognition as sr
from collections import deque
from typing import Callable, Optional

# CUDA DLL paths for faster-whisper
CUDA_BIN_DIRS = [
    r"C:\Users\PC\AppData\Local\Programs\Python\Python312\Lib\site-packages\nvidia\cublas\bin",
    r"C:\Users\PC\AppData\Local\Programs\Python\Python312\Lib\site-packages\nvidia\cudnn\bin",
    r"C:\Users\PC\AppData\Local\Programs\Python\Python312\Lib\site-packages\nvidia\cuda_nvrtc\bin"
]
for d in CUDA_BIN_DIRS:
    if os.path.exists(d):
        try:
            os.add_dll_directory(d)
        except Exception:
            pass
        if d not in os.environ.get("PATH", ""):
            os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH", "")

from faster_whisper import WhisperModel

# Initialize Whisper Large-v3-Turbo
print("[Speech Engine] Faster-Whisper Large-v3-Turbo (809M) ACTIVE on NVIDIA RTX 3070 (CUDA fp16).", flush=True)
try:
    whisper_model = WhisperModel("large-v3-turbo", device="cuda", compute_type="float16")
except Exception as e:
    print(f"[Whisper GPU Init Warning]: {e}. Falling back to float32/CPU...", flush=True)
    try:
        whisper_model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
    except Exception as e2:
        print(f"[Whisper CPU Fallback Error]: {e2}", flush=True)
        whisper_model = None

WAKE_REGEX = re.compile(
    r"\b(eloise|éloïse|eloyse|éloise|heloise|héloïse)\b",
    re.IGNORECASE
)

STOP_REGEX = re.compile(
    r"\b(stop|stoppe|arrête|arrete|arrête-toi|arrete-toi|tais-toi|tais toi|ferme-la|ferme la|chut|shut up|silence|pause)\b",
    re.IGNORECASE
)

PROMPT_CONTEXT = "Éloïse, Hunger, Sarlat Farm, Jacques Bridge, Sombre Forest, Drooler, Brute, Flour, Charcoal, Saltpetre, Jacques Folly, quest, map, raid."
HOTWORDS = "Éloïse Eloise Sarlat Jacques Sombre Drooler Brute Folly Flour Charcoal Saltpetre quest map raid estoc thrust poison antiheal"


class HyperXMicListener:
    """
    High-performance real-time microphone listener using an asynchronous worker queue.
    The SoundDevice audio callback is completely non-blocking, preventing stream buffer
    overflows and eliminating lag between wake-word and command processing.
    """

    def __init__(self,
                 on_wake: Optional[Callable[[str], None]] = None,
                 on_command: Optional[Callable[[str, str], None]] = None,
                 on_heard: Optional[Callable[[str], None]] = None,
                 is_active: Optional[Callable[[], bool]] = None,
                 sample_rate: int = 16000,
                 silence_timeout: float = 1.35):
        self.on_wake = on_wake
        self.on_command = on_command
        self.on_heard = on_heard
        self.is_active = is_active
        self.sample_rate = sample_rate
        self.silence_timeout = silence_timeout
        self.threshold = 220.0
        self.ambient_rms = 180.0
        self.last_callback_time = time.time()
        self.is_running = False
        
        self.audio_queue = queue.Queue()
        self.recognizer = sr.Recognizer()
        self.worker_thread = None
        self.capture_thread = None

    def recalibrate(self, duration: float = 0.8):
        """Recalibrate noise floor and speech gate on demand (e.g. from Discord !reconnect command)."""
        try:
            print("[Microphone] Recalibrating HyperX Headset Mic...", flush=True)
            calib = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='int16')
            sd.wait()
            amb = float(np.sqrt(np.mean(calib[:, 0].astype(np.float32)**2)))
            self.ambient_rms = amb
            self.threshold = max(200.0, min(amb * 1.20, 420.0))
            print(f"[Microphone] Recalibration complete. Ambient: {self.ambient_rms:.1f}, Speech Gate: {self.threshold:.1f}", flush=True)
            return self.threshold
        except Exception as e:
            print(f"[Microphone Recalibration Warning]: {e}", flush=True)
            self.threshold = 240.0
            return self.threshold

    def get_status(self) -> dict:
        """Return diagnostic metrics for !status command."""
        return {
            "is_running": self.is_running,
            "ambient_rms": round(self.ambient_rms, 1),
            "threshold": round(self.threshold, 1),
            "seconds_since_audio": round(time.time() - self.last_callback_time, 1),
            "queue_size": self.audio_queue.qsize()
        }

    def start(self):
        """Start both the background processing worker and audio capture stream."""
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        
        capture_thread = threading.Thread(target=self._run_capture_stream, daemon=True)
        capture_thread.start()

    def _worker_loop(self):
        """Dedicated background worker that transcribes and routes audio without blocking audio capture."""
        while self.is_running:
            try:
                pcm_int16 = self.audio_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            try:
                self._process_recorded_audio(pcm_int16)
            except Exception as e:
                print(f"[Audio Worker Error]: {e}", flush=True)
            finally:
                self.audio_queue.task_done()

    def _run_capture_stream(self):
        pre_roll_buffer = deque(maxlen=int(self.sample_rate * 0.40 / (self.sample_rate * 0.04)))  # ~400ms pre-roll

        # Initial Ambient Calibration
        self.recalibrate(duration=0.8)

        print("\n=======================================================", flush=True)
        print("  🎙️  LIVE MICROPHONE ACTIVE (HyperX Headset)", flush=True)
        print("  Say 'Éloïse' -> She responds 'Oui ?' -> Speak your question!", flush=True)
        print("=======================================================\n", flush=True)

        buffer = []
        is_speaking = False
        last_voice_time = time.time()

        def audio_callback(indata, frames, time_info, status):
            nonlocal is_speaking, last_voice_time, buffer
            if not self.is_running:
                return

            self.last_callback_time = time.time()

            # Check if Eloise is connected to HUNGER voice channel; if not, stay completely dormant!
            if self.is_active and not self.is_active():
                if is_speaking:
                    is_speaking = False
                    buffer = []
                return

            audio_data = indata[:, 0]
            rms = float(np.sqrt(np.mean(audio_data.astype(np.float32)**2)))
            
            if rms > self.threshold:
                if not is_speaking:
                    is_speaking = True
                    buffer = list(pre_roll_buffer)
                    print(f"[Mic] Voice activity detected (RMS: {rms:.0f})...", flush=True)
                last_voice_time = time.time()
                buffer.append(audio_data.copy())
            elif is_speaking:
                buffer.append(audio_data.copy())
                # Allow natural pauses up to silence_timeout
                if time.time() - last_voice_time > self.silence_timeout:
                    is_speaking = False
                    if len(buffer) > 10:  # At least ~0.4s audio
                        recorded_audio = np.concatenate(buffer)
                        # Offload to background queue immediately (callback returns in microseconds)
                        self.audio_queue.put(recorded_audio)
                    buffer = []
            else:
                pre_roll_buffer.append(audio_data.copy())
                # Dynamic noise floor tracking: smooth exponential moving average
                if rms > 15.0:
                    self.ambient_rms = 0.992 * self.ambient_rms + 0.008 * rms
                    self.threshold = max(200.0, min(self.ambient_rms * 1.25, 420.0))

        # Persistent auto-reconnecting stream loop
        while self.is_running:
            try:
                with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype='int16',
                                    blocksize=int(self.sample_rate * 0.04), callback=audio_callback):
                    while self.is_running:
                        sd.sleep(500)
            except Exception as e:
                if self.is_running:
                    print(f"[Microphone Stream Interruption]: {e}. Auto-reconnecting in 2.0s...", flush=True)
                    time.sleep(2.0)

    def _process_recorded_audio(self, pcm_int16: np.ndarray):
        if self.is_active and not self.is_active():
            return

        text = ""
        lang = "en"
        
        # 1. Faster-Whisper Large-v3-Turbo on RTX 3070 CUDA
        if whisper_model is not None:
            try:
                audio_float32 = pcm_int16.astype(np.float32)
                peak = np.max(np.abs(audio_float32))
                if peak > 0:
                    audio_float32 = (audio_float32 / peak) * 0.95
                else:
                    audio_float32 = audio_float32 / 32768.0

                segments, info = whisper_model.transcribe(
                    audio_float32,
                    beam_size=1,
                    initial_prompt=PROMPT_CONTEXT,
                    hotwords=HOTWORDS,
                    vad_filter=True,
                    vad_parameters=dict(min_silence_duration_ms=350),
                    temperature=0.0,
                    condition_on_previous_text=False
                )
                segments_list = list(segments)
                # Filter silent audio where no_speech_prob is high across all segments
                if segments_list and all(s.no_speech_prob > 0.60 for s in segments_list):
                    return

                text = " ".join([s.text for s in segments_list]).strip()
                if info and info.language:
                    lang = info.language
            except Exception as e:
                print(f"[Whisper Error]: {e}", flush=True)

        # 2. Fallback: Google Speech Recognition if Whisper failed
        if not text:
            try:
                raw_bytes = pcm_int16.tobytes()
                wav_io = io.BytesIO()
                with wave.open(wav_io, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(self.sample_rate)
                    wf.writeframes(raw_bytes)
                wav_io.seek(0)
                with sr.AudioFile(wav_io) as source:
                    audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio).strip()
            except Exception:
                pass

        if not text or len(text) < 2:
            return

        # Filter Whisper silent-audio hallucinations
        HALLUCINATION_KEYWORDS = [
            "sous-titrage", "st' 501", "st 501", "amara.org", "transcription",
            "watching", "subscribe", "subtitles", "merci d'avoir regardé",
            "thank you for watching", "namious"
        ]
        lowered_text = text.lower()
        if any(h in lowered_text for h in HALLUCINATION_KEYWORDS):
            return

        # Enforce French / English only: discard any language hallucination like pt, cy, nn, etc.
        if lang not in ["fr", "en"]:
            # If whisper guessed another language on background noise, only proceed if clear game words appear
            if not any(w in lowered_text for w in ["eloise", "éloïse", "hunger", "sarlat", "jacques", "sombre", "folly", "oui", "non", "stop"]):
                return
            lang = "fr" if any(w in lowered_text for w in ["est", "les", "des", "pour", "quoi", "oui", "merci"]) else "en"

        # Discard repetitive loops (e.g. "word word word" or "f f f f")
        if re.search(r"\b(\w+)\b(?:\s+\1\b){2,}", lowered_text):
            return

        print(f"\n>>> [Microphone Heard] (Lang: {lang}): \"{text}\"", flush=True)
        
        # Immediate Emergency Stop detection: always kills speech even without wake-word!
        if STOP_REGEX.search(lowered_text):
            print(f">>> [EMERGENCY STOP DETECTED] Killing speech immediately.", flush=True)
            if self.on_command:
                self.on_command("stop", lang, has_wake=True)
            return

        # Update text channel live status
        if self.on_heard:
            self.on_heard(text)
            
        # Analyze wake word
        has_wake = bool(WAKE_REGEX.search(text))
        remainder = WAKE_REGEX.sub("", text).strip()
        clean_command = re.sub(r"^[,\.\?!;: -]+|[,\.\?!;: -]+$", "", remainder).strip()
        
        # Detect if user is calling her name
        conversational_wake = clean_command.lower() in [
            "", "tu es là", "tu m'entends", "t'es là", "are you there",
            "can you hear me", "hello", "bonjour", "salut", "hey", "oui", "yes"
        ]

        if has_wake and (not clean_command or conversational_wake):
            print(f">>> [Eloise Wake-Word Detected] Confirming listening with 'Oui ?'...", flush=True)
            if self.on_wake:
                self.on_wake(lang)
            return

        # Route command with wake status
        target_command = clean_command if has_wake else text
        print(f">>> [Eloise Mic Event] (Wake={has_wake}): \"{target_command}\"", flush=True)
        if self.on_command:
            self.on_command(target_command, lang, has_wake)

    def stop(self):
        self.is_running = False

LocalMicListener = HyperXMicListener
