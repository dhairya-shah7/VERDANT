"""
V.E.R.D.A.N.T. Desktop Floating Capsule - Voice Ingestion
Captures microphone audio using sounddevice / pyaudio,
encoding into clean 16kHz WAV format for Google Gemini multimodal audio reasoning.
"""
from pathlib import Path
from typing import Optional
import io
import wave
import time
import numpy as np

try:
    import sounddevice as sd
    HAS_SOUNDDEVICE = True
except ImportError:
    HAS_SOUNDDEVICE = False


class VoiceRecorder:
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.recording = False
        self.frames = []
        self._stream = None

    def start_recording(self):
        """Starts capturing microphone audio stream."""
        if not HAS_SOUNDDEVICE:
            print("[Voice] sounddevice not available for audio capture.")
            return

        self.frames = []
        self.recording = True

        def callback(indata, frames, time_info, status):
            if self.recording:
                self.frames.append(indata.copy())

        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            callback=callback
        )
        self._stream.start()

    def stop_recording(self) -> Optional[bytes]:
        """Stops recording and returns standard WAV encoded bytes."""
        if not self.recording or not HAS_SOUNDDEVICE:
            return None

        self.recording = False
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None

        if not self.frames:
            return None

        audio_data = np.concatenate(self.frames, axis=0)

        # Encode to WAV byte buffer
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data.tobytes())

        return wav_buffer.getvalue()
