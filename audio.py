from io import BytesIO
import sounddevice as sd
import numpy as np
import time
import tempfile
import os
import subprocess
import shlex

from kink import inject
from config import Config
from data import Data
from log import Logging
from models import AppState
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
from threading import Thread
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import soundfile as sf


@inject
class Audio:

    def __init__(self, config: Config, data: Data, logging: Logging):
        self._data = data
        self._config = config
        self._logging = logging
        self._elevenlabs_client = ElevenLabs(
            api_key=config.ELEVENLABS_API_KEY,
        )

    def recordAudio(self):
        audioData = []
        self._data.changeAppState(AppState.RECORDING_INPUT)
        blockDuration = self._config.RECORDING_BLOCK_DURATION
        duration = self._config.RECORDING_DURATION
        sampleRate = self._config.RECORDING_SAMPLE_RATE

        def callback(inData, frames, time, status):
            nonlocal audioData
            if self._data.appState == AppState.RECORDING_INPUT:
                audioData.append(inData.copy())

        with sd.InputStream(
            callback=callback,
            samplerate=sampleRate,
            channels=1,
            blocksize=int(sampleRate * blockDuration),
        ):
            while (
                self._data.appState == AppState.RECORDING_INPUT
                and len(audioData) * blockDuration < duration
            ):
                sd.sleep(int(blockDuration * 1000))

        audioData = np.concatenate(audioData, axis=0)
        return audioData, sampleRate

    def transcribeAudioToText(self, audioData, sampleRate):
        startTime = time.time()
        tempDir = "./input/"
        os.makedirs(tempDir, exist_ok=True)
        tempFilePath = tempfile.mktemp(suffix=".wav", dir=tempDir)
        try:
            write(tempFilePath, sampleRate, audioData)
            segments, _ = WhisperModel(
                self._config.WHISPER_MODEL_SIZE,
                device=self._config.WHISPER_DEVICE,
                compute_type=self._config.WHISPER_COMPUTE_TYPE,
            ).transcribe(tempFilePath)

            transcript = " ".join(segment.text for segment in segments)
            self._logging.logUser("User: " + transcript)
            endTime = time.time()
            duration = startTime - endTime
            self._logging.logInfo(f"Transcription: + {duration:.2f} seconds")
            return transcript
        except Exception as e:
            self._logging.logError(f"Error during transcription: {e}")
        finally:
            os.remove(tempFilePath)

    def playOutputAudio(self, text, rate=None):
        if self._config.OFFLINE:
            # Use the passed rate if provided, otherwise use the default from config
            output_rate = (
                rate if rate is not None else self._config.LOCAL_TTS_OUTPUT_RATE
            )
            command = (
                f"say -v {shlex.quote(self._config.LOCAL_TTS_OUTPUT_VOICE)} "
                f"-r {output_rate} {shlex.quote(text)}"
            )
            subprocess.run(command, shell=True, check=True)
        else:
            self.text_to_speech_stream(self._config.ELEVENLABS_OUTPUT_VOICE, text)

    def playInputAudio(self, text, rate=None):
        if self._config.OFFLINE:
            # Use the passed rate if provided, otherwise use the default from config
            input_rate = rate if rate is not None else self._config.LOCAL_TTS_INPUT_RATE
            command = (
                f"say -v {shlex.quote(self._config.LOCAL_TTS_INPUT_VOICE)} "
                f"-r {input_rate} {shlex.quote(text)}"
            )
            subprocess.run(command, shell=True, check=True)
        else:
            self.text_to_speech_stream(self._config.ELEVENLABS_INPUT_VOICE, text)

    def text_to_speech_stream(self, voice_id: str, text: str):
        response = self._elevenlabs_client.text_to_speech.convert(
            voice_id=voice_id,
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",  
            text=text,
            model_id=self._config.ELEVENLABS_MODEL,
            voice_settings=VoiceSettings(
                stability=0.8,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
            ),
        )

        # Create a BytesIO object to hold the audio data in memory
        audio_stream = BytesIO()

        # Write each chunk of audio data to the stream
        for chunk in response:
            if chunk:
                audio_stream.write(chunk)

        # Reset stream position to the beginning
        audio_stream.seek(0)

        # Read the audio data using soundfile
        audio_data, sample_rate = sf.read(audio_stream, dtype="float32")

        # Play the audio
        sd.play(audio_data, sample_rate)
        sd.wait()  # Wait until the audio playback is finished
