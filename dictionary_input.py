from audio import Audio
from config import Config
from gsheet import TranslationSpreadsheet
from llm import Llm
from data import Data
from kink import inject
from models import AppState
from log import Logging

import keyboard
import time


@inject
class DictionaryInput:

    previousState = None

    def __init__(
        self, config: Config, audio: Audio, llm: Llm, data: Data, logging: Logging
    ):
        # init deps
        self._config = config
        self._audio = audio
        self._llm = llm
        self._data = data
        self._logging = logging
        # Log info
        self._logging.logInfo(f"Press the Escape key to start recording")
        self._audio.playInputAudio(f"Hi, let's start")

    def _onEscPress(self, event):
        if event.name == "esc" or event.name == "escape":
            if self._data.appState == AppState.WAITING_FOR_INPUT:
                self._data.changeAppState(AppState.RECORDING_INPUT)
                self._logging.logInfo(
                    "Recording started. Press the escape key to stop."
                )
            elif self._data.appState == AppState.RECORDING_INPUT:
                self._data.changeAppState(AppState.PROCESSING_INPUT)
                self._logging.logInfo("Recording stopped. Processing input...")

    def run(self):

        try:
            keyboard.on_press(self._onEscPress)
            while True:
                if self._data.appState != self.previousState:
                    self.previousState = self._data.appState

                if self._data.appState == AppState.RECORDING_INPUT:
                    # Start recording
                    recording, sampleRate = self._audio.recordAudio()
                    self._data.changeAppState(AppState.PROCESSING_INPUT)

                elif self._data.appState == AppState.PROCESSING_INPUT:
                    # Transcribe and process input
                    transcribedUserInput = self._audio.transcribeAudioToText(
                        recording, sampleRate
                    )
                    self._llm.processResponse(transcribedUserInput)
                    self._data.changeAppState(AppState.GENERATING_OUTPUT)

                elif self._data.appState == AppState.GENERATING_OUTPUT:
                    # Generate output
                    self._data.changeAppState(AppState.WAITING_FOR_INPUT)

                # Add a short sleep to prevent the loop from hogging CPU
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("")
            self._logging.logInfo("Shutting down...")
