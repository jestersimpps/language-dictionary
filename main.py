from audio import Audio
from config import Config
from data import Data
from dictionary_input import DictionaryInput
from gsheet import TranslationSpreadsheet
import inquirer
from interrogate import Interrogation
from llm import Llm
from log import Logging  # type: ignore


def main():
    while True:
        questions = [
            inquirer.List(
                "todo",
                message="Welcome to language tools! Select a option:",
                choices=["add to dictionary", "interrogate", "quit"],
            ),
        ]

        answers = inquirer.prompt(questions)
        selected_answer = answers["todo"]
        
        
        
        if selected_answer == "quit":
            print("Exiting the program.")
            break
          
        if selected_answer == "add to dictionary":
            config = Config()
            logging = Logging()
            gsheet = TranslationSpreadsheet(
                config.GOOGLE_CREDS_FILE, config.GOOGLE_SHEET_ID, config.GOOGLE_EMAIL_ADDRESS
            )
            data = Data(config)
            audio = Audio(config, data, logging)
            llm = Llm(config, data, logging, audio, gsheet)
            dictionaryInput = DictionaryInput(config, audio, llm, data, logging)
            dictionaryInput.run()
            break
          
        if selected_answer == "interrogate":
            config = Config()
            data = Data(config)
            logging = Logging()
            audio = Audio(config, data, logging)
            gsheet = TranslationSpreadsheet(
                config.GOOGLE_CREDS_FILE, config.GOOGLE_SHEET_ID, config.GOOGLE_EMAIL_ADDRESS
            )
            interrogation = Interrogation(gsheet, audio, logging)
            interrogation.run()
            break



main()
