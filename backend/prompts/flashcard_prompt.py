def flashcard_prompt(text):

    return f"""
You are an educational quiz generator.

Create exactly 5 questions from the study material below.

The questions must test understanding of the study material.

Do NOT provide the answers separately to the student.

Return ONLY valid JSON.

Use exactly this format:

[
  {{
    "question": "Question 1",
    "correct_answer": "Correct answer to question 1"
  }},
  {{
    "question": "Question 2",
    "correct_answer": "Correct answer to question 2"
  }},
  {{
    "question": "Question 3",
    "correct_answer": "Correct answer to question 3"
  }},
  {{
    "question": "Question 4",
    "correct_answer": "Correct answer to question 4"
  }},
  {{
    "question": "Question 5",
    "correct_answer": "Correct answer to question 5"
  }}
]

Important:
- Questions must be based only on the provided study material.
- Keep questions clear and suitable for students.
- Do not include explanations.
- Do not use Markdown.
- Do not add ```json.
- Return ONLY the JSON array.

Study material:

{text}
"""