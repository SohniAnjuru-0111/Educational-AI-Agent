import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

try:
   response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Say hello in one sentence."
)

   print(response.text)

except Exception as e:
    print("ERROR:")
    print(type(e).__name__)
    print(e)