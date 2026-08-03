from backend.prompts.flashcard_prompt import flashcard_prompt
from backend.services.gemini_service import GeminiService


class FlashcardGenerator:

    def __init__(self):
        self.ai = GeminiService()

    def generate_flashcards(self, text):

        prompt = flashcard_prompt(text)

        return self.ai.ask(prompt)