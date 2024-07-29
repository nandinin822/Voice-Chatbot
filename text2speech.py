import os
from dotenv import load_dotenv
from deepgram import Deepgram
from deepgram import DeepgramClient, SpeakOptions

load_dotenv()

def text_to_speech(text, filename="output.wav"):
    try:
        api_key = os.getenv("DG_API_KEY")
        if not api_key:
            raise ValueError("Deepgram API key not set in environment variables.")

        SPEAK_OPTIONS = {"text": text}

        deepgram = DeepgramClient(api_key=api_key)

        options = SpeakOptions(
            model="aura-asteria-en",
            encoding="linear16",
            container="wav"
        )

        response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)
        return filename

    except Exception as e:
        print(f"Exception: {e}")
        return None
