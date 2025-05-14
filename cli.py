from app.ai_utils import get_command_from_natural_language
from app.commands import handle_command

while True:
    user_input = input(">>> ")
    if user_input.lower() == "exit":
        print("Exiting...")
        break

    # Convert NLP input to structured command
    command = get_command_from_natural_language(user_input)
    if command == "invalid":
        print("Sorry, I didn't understand that.")
    else:
        handle_command(command)
    print("="*50)
