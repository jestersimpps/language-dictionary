from kink import inject
from models import LogLevel

@inject
class Config:
  
  INPUT_LANGUAGE = "german"
  OUTPUT_LANGUAGE = "english"
  WELCOME_MESSAGE = "Guten Tag! Ich freue mich, dass wir auf Deutsch beginnen. Drücken Sie die Escape-Taste, um die Aufnahme zu starten."
  
  def create_instructions(self, input_language, output_language, prompt):
      INSTRUCTIONS = f"""You are an {input_language} to {output_language} translator. 
        Give me the translation of the following: "{prompt}" in {output_language}. 
        Below are examples of possible responses in the format I want you to respond in:
        
        {{
        "prompt": "Apfel",
        "translation": "apple",
        "gender": "masculine",
        "root": "From Old High German 'apful', from Proto-Germanic '*aplaz'",
        "example": "Ich esse jeden Tag einen Apfel."
        }}

        {{
        "prompt": "laufen",
        "translation": "to run, to walk",
        "root": "From Middle High German 'loufen', from Old High German 'loufan'",
        "example": "Sie läuft jeden Morgen im Park."
        }}

        {{
        "prompt": "Buch",
        "translation": "book",
        "gender": "neuter",
        "root": "From Old High German 'buoh', from Proto-Germanic '*bōks'",
        "example": "Das Buch auf dem Tisch gehört mir."
        }}

        {{
        "prompt": "schön",
        "translation": "beautiful, nice",
        "root": "From Middle High German 'schœne', from Old High German 'scōni'",
        "example": "Das ist ein schöner Tag heute."
        }}
        
        """
      return INSTRUCTIONS
  
  # TTS
  LOCAL_TTS_VOICE="com.apple.speech.synthesis.voice.anna.premium"
  LOCAL_TTS_RATE=180

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

