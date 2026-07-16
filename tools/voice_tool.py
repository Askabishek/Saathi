import os
from openai import OpenAI
from gtts import gTTS
import tempfile

class VoiceTool:
    def __init__(self, api_key=None):
        self.client = groq(api_key=os.environ.get("GROQ_API_KEY"))

    def stt(self, audio_file_path):
        try:
            with open(audio_file_path, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file=(os.path.basename(audio_file_path), file.read()),
                    model="whisper-large-v3-turbo",
                )
            return transcription.text
        except Exception as e:
            return f"STT Error: {str(e)}"

    def tts(self, text, output_path="speech.mp3"):
        try:
            tts = gTTS(text=text, lang='en')
            tts.save(output_path)
            return output_path
        except Exception as e:
            print(f"TTS Error: {str(e)}")
            return None
