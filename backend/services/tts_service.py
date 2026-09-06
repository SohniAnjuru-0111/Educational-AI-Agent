import os
from gtts import gTTS


class TTSService:

    def generate_audio(self, text):

        if not text or not text.strip():
            return None

        try:

            os.makedirs(
                "data/audio",
                exist_ok=True
            )

            audio_path = "data/audio/answer.mp3"

            tts = gTTS(
                text=text,
                lang="en"
            )

            tts.save(audio_path)

            if os.path.exists(audio_path):
                return audio_path

            return None

        except Exception as e:

            print("TTS error:", e)

            return None