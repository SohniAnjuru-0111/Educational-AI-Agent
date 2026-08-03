from backend.prompts.evaluation_prompt import evaluation_prompt
from backend.services.gemini_service import GeminiService


class QuizEvaluator:

    def __init__(self):
        self.ai = GeminiService()

    def evaluate(self, quiz, answers):

        prompt = evaluation_prompt(
            quiz,
            answers
        )

        return self.ai.ask(prompt)