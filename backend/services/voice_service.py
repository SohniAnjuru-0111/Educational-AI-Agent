import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av


class AudioProcessor(AudioProcessorBase):

    def __init__(self):
        self.audio_frames = []

    def recv(self, frame):

        self.audio_frames.append(frame)

        return frame


class VoiceService:

    def __init__(self):

        self.recognizer = sr.Recognizer()

    def start_recording(self):

        ctx = webrtc_streamer(
            key="voice-recorder",
            audio_processor_factory=AudioProcessor,
            media_stream_constraints={
                "audio": True,
                "video": False
            }
        )

        return ctx

    def convert_to_text(self, ctx):

        if ctx is None:
            return ""

        processor = ctx.audio_processor

        if processor is None:
            return ""

        frames = processor.audio_frames

        if not frames:
            return ""

        try:

            # Convert WebRTC audio to
            # mono, 16-bit, 16 kHz PCM
            resampler = av.AudioResampler(
                format="s16",
                layout="mono",
                rate=16000
            )

            audio_bytes = b""

            for frame in frames:

                converted_frames = resampler.resample(frame)

                for converted_frame in converted_frames:

                    audio_array = converted_frame.to_ndarray()

                    audio_bytes += audio_array.tobytes()

            if not audio_bytes:

                return ""

            # Create SpeechRecognition AudioData
            audio = sr.AudioData(
                audio_bytes,
                16000,
                2
            )

            # Convert speech to text
            text = self.recognizer.recognize_google(
                audio
            )

            return text

        except sr.UnknownValueError:

            return ""

        except sr.RequestError as e:

            print(
                "Google Speech Recognition error:",
                e
            )

            return ""

        except Exception as e:

            print(
                "Voice conversion error:",
                e
            )

            return ""