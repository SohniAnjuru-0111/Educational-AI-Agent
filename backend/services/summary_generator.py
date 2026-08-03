from backend.services.gemini_service import GeminiService


class SummaryGenerator:

    def __init__(self):

        self.gemini = GeminiService()

    def generate_summary(self, text):

        prompt = f"""
You are an expert teacher.

Summarize the following study material.

Requirements:

- Simple English
- Bullet Points
- Headings
- Important Facts
- Exam Tips
- Key Concepts

Study Material:

{text}
"""

        return self.gemini.ask(prompt)