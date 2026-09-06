import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Please add it to your .env file."
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def ask(self, prompt):

        if not prompt or not prompt.strip():
            return "⚠️ Please provide a valid prompt."

        for attempt in range(3):

            try:

                response = self.client.models.generate_content(
                    model="gemini-3.1-flash-lite",
                    contents=prompt,
                )

                if response and response.text:
                    return response.text

                return "⚠️ Gemini returned an empty response."

            except Exception as e:

                error_message = str(e)

                if "503" in error_message or "429" in error_message:

                    if attempt < 2:
                        time.sleep(5)
                        continue

                    return (
                        "⚠️ Gemini is currently busy. "
                        "Please try again in a few moments."
                    )

                if "401" in error_message or "403" in error_message:
                    return (
                        "⚠️ Gemini API authentication failed. "
                        "Please check your GEMINI_API_KEY."
                    )

                return (
                    "⚠️ Unable to connect to Gemini right now. "
                    "Please try again."
                )

        return "⚠️ Gemini server is busy. Please try again."

    def ask_from_context(self, context, question):

        if not context or not context.strip():
            return "⚠️ No document context is available."

        if not question or not question.strip():
            return "⚠️ Please enter a question."

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

        try:

            response = self.client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt,
            )

            if response and response.text:
                return response.text

            return "⚠️ Gemini returned an empty response."

        except Exception as e:

            error_message = str(e)

            if "429" in error_message:
                return "⚠️ Gemini rate limit reached. Please try again later."

            if "503" in error_message:
                return "⚠️ Gemini server is temporarily busy. Please try again."

            if "401" in error_message or "403" in error_message:
                return (
                    "⚠️ Gemini API authentication failed. "
                    "Please check your GEMINI_API_KEY."
                )

            return (
                "⚠️ Unable to get an answer from Gemini. "
                "Please try again."
            )