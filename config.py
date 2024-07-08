from kink import inject
from models import LogLevel
from dotenv import load_dotenv  # type: ignore
import os


load_dotenv()


@inject
class Config:

    INPUT_LANGUAGE = "english"
    OUTPUT_LANGUAGE = "chinese"

    def create_dictionary_instructions(self, input_language, output_language, prompt):
        INSTRUCTIONS = f"""
        You are an {input_language} to {output_language} translator. 
        Give me the translation of the following: "{prompt}" in {output_language}. 
        Below are examples of possible responses in the format I want you to respond in:
        
        {{
        "prompt": "Calculator",
        "translation": "计算器",
        "pinyin": "jìsuànqì",
        "notes": "计 (jì): to calculate; 算 (suàn): to compute; 器 (qì): device/tool"
        }}

        {{
        "prompt": "House",
        "translation": "房子",
        "pinyin": "fángzi",
        "notes": "房 (fáng): house/room; 子 (zi): noun suffix"
        }}

        {{
        "prompt": "Train",
        "translation": "火车或教练",
        "pinyin": "huǒchē huò jiàoliàn",
        "notes": "火 (huǒ): fire; 车 (chē): vehicle; 或 (huò): or; 教 (jiào): teach; 练 (liàn): practice/train"
        }}

        {{
        "prompt": "I am tired",
        "translation": "我很疲勒",
        "pinyin": "wǒ hěn pí lè",
        "notes": "我 (wǒ): I/me; 很 (hěn): very; 疲 (pí): tired; 勒 (lè): tired/weary"
        }}
        """
        return INSTRUCTIONS

    # def create_dictionary_instructions(self, translation, transcribedUserInput):
    #     INSTRUCTIONS = f"""
    #     would you be able to understand someone "{transcribedUserInput}" 
    #     if you are a native chinese speaker
    #     and they meant "{translation}"

    #     """
    #     return INSTRUCTIONS
    # LOCAL TTS
    LOCAL_TTS_INPUT_VOICE = "com.apple.speech.synthesis.voice.joelle"
    LOCAL_TTS_INPUT_RATE = 160

    LOCAL_TTS_OUTPUT_VOICE = "com.apple.speech.synthesis.voice.tingting"
    LOCAL_TTS_OUTPUT_RATE = 60

    # LOCAL LLM
    LOCAL_OLLAMA_LLM = "phi3"
    OFFLINE = False

    # OPEN AI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # ELEVENLABS TTS
    ELEVENLABS_API_KEY= os.getenv("ELEVENLABS_API_KEY")
    ELEVENLABS_INPUT_VOICE = "RPdRfxxQOaNxn1LtRQqm"
    ELEVENLABS_OUTPUT_VOICE = "ByhETIclHirOlWnWKhHc"
    ELEVENLABS_MODEL = "eleven_turbo_v2"

    # Google Sheet
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
    GOOGLE_CREDS_FILE = "credentials.json"
    GOOGLE_EMAIL_ADDRESS = os.getenv("GOOGLE_EMAIL_ADDRESS")

    # Recording
    RECORDING_SAMPLE_RATE = 44100
    RECORDING_DURATION = 90  # Seconds
    RECORDING_BLOCK_DURATION = 0.1  # Seconds

    # Whisper
    WHISPER_MODEL_SIZE = "small"
    WHISPER_DEVICE = "cpu"
    WHISPER_COMPUTE_TYPE = "float32"

    LOG_LEVEL = LogLevel.INFO
