import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class StudyPlanner:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def generate_plan(
        self,
        subjects,
        exam_date,
        study_hours
    ):

        prompt = f"""
You are an expert AI Study Planner.

Create a realistic and balanced study plan for a student.

Subjects:
{subjects}

Exam Date:
{exam_date}

Available Study Hours Per Day:
{study_hours}

Create the plan with:

1. Daily schedule
2. Subject/topic for each day
3. Recommended study hours
4. Revision sessions
5. Practice/test sessions
6. Important final revision before the exam

Make the plan practical and easy to follow.

Use clear headings and tables where appropriate.
"""

        response = self.client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        return response.text