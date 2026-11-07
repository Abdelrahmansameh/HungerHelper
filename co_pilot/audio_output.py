import os
import asyncio
import subprocess
import threading
import winsound
import edge_tts
import imageio_ffmpeg
import re

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
DEFAULT_VOICE = "fr-FR-VivienneMultilingualNeural"

_current_play_lock = threading.Lock()
_playback_id = 0

def stop_audio():
    """Immediately kill any audio playing in local headset/speakers."""
    global _playback_id
    with _current_play_lock:
        _playback_id += 1
    try:
        winsound.PlaySound(None, winsound.SND_PURGE)
    except Exception:
        pass

async def _synthesize_and_convert(text: str, wav_path: str, voice: str):
    clean = re.sub(r"[\*#_~`\|]+", " ", text)
    clean = re.sub(r"[^\w\s\.,\?!'-]", " ", clean).strip()
    clean = re.sub(r"\s+", " ", clean).strip()
    if not clean:
        return False
        
    mp3_path = wav_path.replace(".wav", ".mp3")
    comm = edge_tts.Communicate(clean, voice)
    await comm.save(mp3_path)
    
    subprocess.run(
        [FFMPEG_EXE, "-y", "-i", mp3_path, wav_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if os.path.exists(mp3_path):
        try:
            os.remove(mp3_path)
        except OSError:
            pass
    return os.path.exists(wav_path)

def _play_thread(text: str, wav_path: str, voice: str, this_id: int):
    try:
        success = asyncio.run(_synthesize_and_convert(text, wav_path, voice))
        if not success:
            return
            
        with _current_play_lock:
            # If interrupted or a newer playback started, discard
            if this_id != _playback_id:
                return

        if os.path.exists(wav_path):
            winsound.PlaySound(wav_path, winsound.SND_FILENAME)
    except Exception as e:
        print(f"[Audio Output Error]: {e}", flush=True)

def speak_async(text: str, voice: str = DEFAULT_VOICE):
    """Synthesize neural speech and play asynchronously out of speakers/headphones."""
    global _playback_id
    stop_audio()  # Stop prior sound before playing new sound
    with _current_play_lock:
        _playback_id += 1
        my_id = _playback_id

    temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "temp_audio"))
    os.makedirs(temp_dir, exist_ok=True)
    wav_path = os.path.join(temp_dir, f"tactical_voice_{my_id}.wav")
    
    t = threading.Thread(target=_play_thread, args=(text, wav_path, voice, my_id), daemon=True)
    t.start()

if __name__ == "__main__":
    print("Testing local voice speech output...")
    speak_async("Bienvenue au chateau, monsieur. Éloïse à votre service.")
