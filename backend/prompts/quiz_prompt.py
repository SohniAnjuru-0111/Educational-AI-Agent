def quiz_prompt(text):

    return f"""
You are an expert teacher.

Study the following notes carefully.

Generate:

# Multiple Choice Questions

Create 10 MCQs.

Each MCQ should have

A)
B)
C)
D)

Mention the correct answer.

--------------------------

# True / False

Generate 5 questions.

Mention answer.

--------------------------

# Fill in the blanks

Generate 5 questions.

Mention answer.

--------------------------

# Short Answer Questions

Generate 5 questions.

Keep answers under 40 words.

Study Material:

{text}
"""