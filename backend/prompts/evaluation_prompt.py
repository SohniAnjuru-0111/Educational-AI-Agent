def evaluation_prompt(questions, answers):

    return f"""
You are an expert teacher.

Evaluate the student's quiz answers.

Return:

1. Total Score
2. Percentage
3. Correct Answers
4. Wrong Answers
5. Explain each wrong answer briefly.
6. Give study suggestions.

Quiz:

{questions}

Student Answers:

{answers}
"""