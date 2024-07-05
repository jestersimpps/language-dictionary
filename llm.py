from kink import inject
from langchain_community.llms import Ollama
from audio import Audio
from config import Config
from data import Data
from log import Logging
from models import Entity
import json
from typing import List, Any

@inject
class Llm:
    def __init__(self, config: Config, data: Data, logging: Logging, audio: Audio):
        self._config = config
        self._data = data
        self._logging = logging
        self._audio = audio

        if config.OFFLINE:
            self._llm = Ollama(model=config.LOCAL_OLLAMA_LLM)
        else:
            # We will include cloud based LLMs here in the future
            pass

    @staticmethod
    def extract_text_from_generations(generations: List[List[Any]]) -> str:
        if generations and generations[0] and generations[0][0].text:
            return generations[0][0].text
        return ""

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
            llmResult = self._llm.generate([prompt_text])
            llmResponse = self.extract_text_from_generations(llmResult.generations)

            self._logging.logLlm(llmResponse)

            try:
                parsed_content = json.loads(llmResponse)
                prompText = parsed_content.get("prompt", "")
                translation = parsed_content.get("translation", "")
                gender = parsed_content.get("gender", "")
                root = parsed_content.get("root", "")
                example = parsed_content.get("example", "")

                if translation:
                    self._audio.playAudio(translation)
                    self._data.addTranslation(prompText, translation, gender, root, example)
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
                        prompText = parsed_content.get("prompt", "")
                        translation = parsed_content.get("translation", "")
                        gender = parsed_content.get("gender", "")
                        root = parsed_content.get("root", "")
                        example = parsed_content.get("example", "")
                        if translation:
                            self._audio.playAudio(translation)
                            self._data.addTranslation(prompText, translation, gender, root, example)
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
