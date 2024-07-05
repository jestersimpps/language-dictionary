from kink import inject
from models import LogLevel

@inject
class Config:
  
  INPUT_LANGUAGE = "english"
  OUTPUT_LANGUAGE = "chinese"
  
  def create_instructions(self, input_language, output_language, prompt):
      INSTRUCTIONS = f"""You are an {input_language} to {output_language} translator. 
        Give me the translation of the following: "{prompt}" in {output_language}. 
        Below are examples of possible responses in the format I want you to respond in:
        
        {{ 
        "prompt": "Calculator", 
        "translation": "计算器", 
        "pinyin": "jìsuànqì",
        "notes": "calculator as in a device, not a person"
        }}
        
        {{ 
        "prompt": "House", 
        "translation": "房子", 
        "pinyin": "fángzi",
        "notes": "house as in a building, not a family"
        }}
        
        {{
        "prompt": "Train",
        "translation": "火车或教练",
        "pinyin": "huǒchē huò jiàoliàn",
        "notes": "train as in a vehicle or a teacher"
        }}
        
        {{
        "prompt": "I am tired",
        "translation": "我很疲勒",
        "pinyin": "wǒ hěn pí lè",
        "notes": "I am tired, in this context, translates directly to '我很疲勒'."
        }}"""
      return INSTRUCTIONS
  
  # TTS
  LOCAL_TTS_VOICE="com.apple.speech.synthesis.voice.meijia"
  LOCAL_TTS_RATE=160

  # LLM
  LOCAL_OLLAMA_LLM = "phi3"
  OFFLINE = True
  
  # Google Sheet
  GOOGLE_SHEET_ID = "1tI3ypTtauyay6t3I2jXOiue_fPWpHCNxrl1Yb3gFUzo"
  GOOGLE_CREDS_FILE = "credentials.json"
  GOOGLE_EMAIL_ADDRESS = "jozzzzen@gmail.com"
  
  
  # Recording
  RECORDING_SAMPLE_RATE = 44100
  RECORDING_DURATION = 90  # Seconds
  RECORDING_BLOCK_DURATION = 0.1  # Seconds
  
  # Whisper
  WHISPER_MODEL_SIZE = "small"
  WHISPER_DEVICE = "cpu"
  WHISPER_COMPUTE_TYPE = "float32"
  
  LOG_LEVEL = LogLevel.INFO

