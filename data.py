from kink import inject
from config import Config
from models import Entity, AppState, LogLevel


@inject
class Data:

    logLevel = LogLevel.INFO
    appState = AppState.WAITING_FOR_INPUT

    def __init__(self, config: Config):
        self.logLevel = config.LOG_LEVEL

    def setRecordingFinished(self):
        self.isRecordingFinished = True
        if self.logLevel == 0:
            print("Recording finished")

    def changeAppState(self, state: AppState):
        self.appState = state
        if self.logLevel == 0:
            print(f"App state changed to {state}")
