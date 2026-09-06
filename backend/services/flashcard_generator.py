import json

from backend.prompts.flashcard_prompt import flashcard_prompt
from backend.services.gemini_service import GeminiService


class FlashcardGenerator:

    def __init__(self):
        self.ai = GeminiService()

    def generate_flashcards(self, text):

        prompt = flashcard_prompt(text)

        response = self.ai.ask(prompt)

        response = response.strip()

        if response.startswith("```"):

            response = response.replace(
                "```json",
                ""
            )

            response = response.replace(
                "```",
                ""
            )

            response = response.strip()

        flashcards = json.loads(response)

        if isinstance(flashcards, dict):

            flashcards = flashcards.get(
                "flashcards",
                [flashcards]
            )

        if not isinstance(flashcards, list):

            raise ValueError(
                "Invalid flashcard format returned by AI."
            )

        return flashcards