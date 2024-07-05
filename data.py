from kink import inject
from config import Config
from gsheet import TranslationSpreadsheet
from models import Entity, AppState, LogLevel


@inject
class Data:
  
    logLevel = LogLevel.INFO
    appState = AppState.WAITING_FOR_INPUT

    def __init__(self, config: Config, gsheet: TranslationSpreadsheet):
        self.logLevel = config.LOG_LEVEL
        self._gsheet = gsheet

    def setRecordingFinished(self):
        self.isRecordingFinished = True
        if self.logLevel == 0:
            print("Recording finished")

    def changeAppState(self, state: AppState):
        self.appState = state
        if self.logLevel == 0:
            print(f"App state changed to {state}")
            
    def addTranslation(self, prompt, translation, gender, root, example):
        self._gsheet.add_translation(prompt, translation, gender, root, example)
