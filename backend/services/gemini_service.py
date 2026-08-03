import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiService:

    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def ask(self, prompt):

        for attempt in range(3):

            try:

                response = self.client.models.generate_content(
                    model="gemini-3.1-flash-lite",
                    contents=prompt,
                )

                return response.text

            except Exception as e:

                if "503" in str(e):
                    time.sleep(5)
                    continue

                raise

        return "⚠️ Gemini server is busy. Please try again."

    def ask_from_context(self, context, question):

        prompt = f"""
You are an Educational AI Tutor.

Answer ONLY using the information in the context below.

If the answer is not available in the context, reply exactly:

"I couldn't find this information in the uploaded PDF."

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
        )

        return response.text