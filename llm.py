from kink import inject
from langchain_community.llms import Ollama
from audio import Audio
from config import Config
from data import Data
from gsheet import TranslationSpreadsheet
from log import Logging
from typing import List, Any
from openai import OpenAI  # type: ignore
import json

@inject
class Llm:
    def __init__(
        self,
        config: Config,
        data: Data,
        logging: Logging,
        audio: Audio,
        gsheet: TranslationSpreadsheet,
    ):
        self._config = config
        self._data = data
        self._logging = logging
        self._audio = audio
        self._gsheet = gsheet

        if config.OFFLINE:
            self._llm = Ollama(model=config.LOCAL_OLLAMA_LLM)
        else:
            self._llm = OpenAI(api_key=config.OPENAI_API_KEY)

    @staticmethod
    def extract_text_from_generations(generations: List[List[Any]]) -> str:
        if generations and generations[0] and generations[0][0].text:
            return generations[0][0].text
        return ""

    def generate_response(self, prompt_text):
        try:
            if self._config.OFFLINE:
                llmResult = self._llm.generate([prompt_text])
                return self.extract_text_from_generations(llmResult.generations)

            else:
                response = self._llm.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt_text}],
                )

                return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error during LLM response generation: {str(e)}")
            return None

    def processResponse(self, prompt: str) -> str:
        prompt = prompt.strip()

        if not prompt:
            self._logging.logInfo("Received empty input, skipping...")
            return

        try:
            print("")

            prompt_text = self._config.create_instructions(
                self._config.INPUT_LANGUAGE, self._config.OUTPUT_LANGUAGE, prompt
            )

            llmResponse = self.generate_response(prompt_text)

            self._logging.logLlm(llmResponse)

            try:
                parsed_content = json.loads(llmResponse)
                english = parsed_content.get("prompt", "")
                translation = parsed_content.get("translation", "")
                pinyin = parsed_content.get("pinyin", "")
                notes = parsed_content.get("notes", "")

                if translation:
                    self._audio.playOutputAudio(translation)
                    self._gsheet.add_translation(english, translation, pinyin, notes)
                else:
                    print("Translation not found in the response.")
            except json.JSONDecodeError:
                print("Failed to parse the response as JSON.")
                # Fallback: try to extract content between curly braces
                start = llmResponse.find("{")
                end = llmResponse.rfind("}")
                if start != -1 and end != -1:
                    json_content = llmResponse[start : end + 1]
                    try:
                        parsed_content = json.loads(json_content)
                        english = parsed_content.get("prompt", "")
                        translation = parsed_content.get("translation", "")
                        pinyin = parsed_content.get("pinyin", "")
                        notes = parsed_content.get("notes", "")
                        if translation:
                            self._audio.playOutputAudio(translation)
                            self._data.addTranslation(english, translation, pinyin, notes)
                        else:
                            print("Translation not found in the extracted JSON.")
                    except json.JSONDecodeError:
                        print("Failed to parse the extracted content as JSON.")
                else:
                    print("No valid JSON object found in the response.")

            print("")

        except Exception as e:
            self._logging.logError(f"Error during LLM response: {e}")

        return llmResponse
