import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

API_KEY = os.environ.get("ELEVEN_LABS_API_KEY")
VOICE_ID = os.environ.get("ELEVEN_LABS_VOICE_ID")
URL = os.environ.get("ELEVEN_LABS_URL")
TEXT_TO_SPEECH_ENDPOINT = "v1/text-to-speech/"