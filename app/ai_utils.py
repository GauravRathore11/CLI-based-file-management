from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)

def get_command_from_natural_language(prompt: str) -> str:
    instruction = """
    You are an AI assistant for a CLI file manager. Convert the user's natural language message into one of the following command formats ONLY:

    - search <name>
    - create file <filename>
    - rename file <prev> <new>
    - delete file <filename>
    - move file <src> <dest>
    - copy file <src> <dest>
    - open file <filename>
    - create folder <foldername>
    - move folder <src> <dest>
    - copy folder <src> <dest>
    - rename folder <prev> <new>
    - delete folder <foldername>
    - compress folder <foldername>
    - change directory <foldername>
    - file info <filename>
    - list
    - help
    - exit

    Only return a valid command from the list above. Do not return any explanations or extra text.

    If the input is unrelated or cannot be matched to any of the above, reply with: invalid
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=f"{instruction}\nUser: {prompt}"
    )
    return response.text.strip().lower()
