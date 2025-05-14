from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)

def get_command_from_natural_language(prompt: str) -> str:
    instruction = """
    You are an AI assistant for a CLI file manager. Convert the user's message into one of the following command formats only:
    - create file <filename>
    - delete file <filename>
    - move file <src> <dest>
    - copy file <src> <dest>
    - list
    - search file <filename>
    - exit
    - help

    If the input is unrelated, reply with: invalid
    """
    response = client.models.generate_content(
        model="gemini-1.5-flash",  # or "gemini-2.0-flash"
        contents=f"{instruction}\nUser: {prompt}"
    )
    return response.text.strip().lower()
