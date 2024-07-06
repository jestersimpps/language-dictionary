import random
from audio import Audio
from gsheet import TranslationSpreadsheet
from log import Logging
import time
import keyboard


class Interrogation:
    def __init__(self, gsheets: TranslationSpreadsheet, audio: Audio, logging: Logging):
        self.questions = []
        self.answers = []
        self.correct = 0
        self.incorrect = 0
        self.total = 0
        self._logging = logging
        self._gsheets = gsheets
        self._audio = audio
        self._rows = gsheets.get_last_row()

    def askQuestion(self, random_row):
        question = random_row["prompt"]

        self._logging.logInfo(question)
        self._audio.playInputAudio(question)
        # wait for space press to continute loop

    def checkAnswer(self, random_row):
        answer = random_row["translation"]
        pinyin = random_row["pinyin"]
        notes = random_row["notes"]

        self._logging.logLlm(answer + "  (" + pinyin + ")   " + notes)
        self._audio.playOutputAudio(answer)

    def run(self):
        while True:
            print("")
            random_row_number = random.randint(1, self._rows - 2)
            random_row = self._gsheets.get_translations()[random_row_number]
            self.askQuestion(random_row)
            keyboard.wait("space")
            self.checkAnswer(random_row)
            time.sleep(0.1)
