from backend.prompts.quiz_prompt import quiz_prompt
from backend.services.gemini_service import GeminiService


class QuizGenerator:

    def __init__(self):

        self.ai = GeminiService()

    def generate_quiz(self, text):

        prompt = quiz_prompt(text)

        return self.ai.ask(prompt)