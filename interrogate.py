import random
from audio import Audio
from data import Data
from gsheet import TranslationSpreadsheet
from log import Logging
import time
import keyboard
from models import AppState


class Interrogation:

    previousState = None

    def __init__(
        self,
        gsheets: TranslationSpreadsheet,
        audio: Audio,
        logging: Logging,
        data: Data,
    ):
        self.correct = 0
        self.incorrect = 0
        self.total = 0
        self._logging = logging
        self._gsheets = gsheets
        self._audio = audio
        self._data = data
        self._rows = gsheets.get_last_row()

    def askQuestion(self, random_row):
        question = random_row["prompt"]
        print("")

        self._logging.logInfo(question)
        self._audio.playInputAudio(question)
        # self._logging.logInfo(f"Press the space key to record your answer")
        self._logging.logInfo(f"Press the space key to show the answer")

        # wait for space press to continute loop

    def checkAnswer(self, random_row, transcribedUserInput):
        answer = random_row["translation"]
        pinyin = random_row["pinyin"]
        notes = random_row["notes"]

        self._logging.logLlm(answer + "  (" + pinyin + ")   " + notes)
        self._audio.playOutputAudio(answer)

    def _onSpacePress(self, event):
        if event.name == "space":
            if self._data.appState == AppState.WAITING_FOR_INPUT:
                self._data.changeAppState(AppState.RECORDING_INPUT)
                self._logging.logInfo("Recording started. Press the space key to stop.")

            elif self._data.appState == AppState.RECORDING_INPUT:
                self._data.changeAppState(AppState.PROCESSING_INPUT)
                self._logging.logInfo("Recording stopped. Processing input...")

    def run(self):
        while True:
            random_row_number = random.randint(1, self._rows - 2)
            random_row = self._gsheets.get_translations()[random_row_number]
            self.askQuestion(random_row)
            keyboard.wait("space")
            self.checkAnswer(random_row, "")

        random_row = None
        try:
            keyboard.on_press(self._onSpacePress)
            random_row_number = random.randint(1, self._rows - 2)
            random_row = self._gsheets.get_translations()[random_row_number]
            self.askQuestion(random_row)
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
                    self.checkAnswer(random_row, transcribedUserInput)
                    self._data.changeAppState(AppState.GENERATING_OUTPUT)

                elif self._data.appState == AppState.GENERATING_OUTPUT:
                    # Generate output
                    random_row_number = random.randint(1, self._rows - 2)
                    random_row = self._gsheets.get_translations()[random_row_number]
                    self.askQuestion(random_row)
                    self._data.changeAppState(AppState.WAITING_FOR_INPUT)

                # Add a short sleep to prevent the loop from hogging CPU
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("")
            self._logging.logInfo("Shutting down...")
