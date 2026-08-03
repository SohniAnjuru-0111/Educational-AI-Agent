def flashcard_prompt(text):

    return f"""
You are an expert teacher.

Read the following study material.

Generate 15 flashcards.

Each flashcard must have:

Question:
Answer:

Keep answers short.

Study Material:

{text}
"""