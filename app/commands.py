import os
import shutil
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)

def show_help():
    print("\n👋 Welcome to Smart CLI!")
    print("You can manage your files and folders using plain English. Just type what you want to do.")
    print("\nHere are some things you can ask me to do:\n")
    print("  • Create a file called 'notes.txt'")
    print("  • Delete the file 'old_report.pdf'")
    print("  • Move 'file1.txt' to the 'Documents' folder")
    print("  • Copy 'image.jpg' to 'Backup' folder")
    print("  • Show all files in the current folder")
    print("  • Create a new folder named 'Projects'")
    print("  • Rename the folder 'New Folder' to '2025 Projects'")
    print("  • Delete the folder called 'Temp'")
    print("  • Rename the file 'draft.docx' to 'final.docx'\n")
    print("Other commands:")
    print("  help      → Show this help message")
    print("  exit      → Exit Smart CLI\n")

def handle_command(command):
    parts = command.split()
    if not parts:
        print("Empty command.")
        return

    if command.startswith("search "):
        filename = command[len("search "):].strip()
        found = False
        for root, dirs, files in os.walk("."):
            if filename in files:
                print(f"Found '{filename}' in: {os.path.join(root, filename)}")
                found = True
        if not found:
            print(f"'{filename}' not found.")

    elif command.startswith("create file "):
        filename = command[len("create file "):].strip()
        if os.path.exists(filename):
            print(f"'{filename}' already exists.")
        else:
            open(filename, "w").close()
            print(f"'{filename}' has been created!")

    elif command.startswith("rename file "):
        _, _, old_name, new_name = parts
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
            print(f"Renamed '{old_name}' to '{new_name}'")
        else:
            print(f"No such file: '{old_name}'")

    elif command.startswith("delete file "):
        filename = command[len("delete file "):].strip()
        if os.path.exists(filename):
            os.remove(filename)
            print(f"'{filename}' has been deleted.")
        else:
            print(f"No such file: '{filename}'")

    elif command.startswith("move file "):
        try:
            _, _, src, dest = parts
            shutil.move(src, dest)
            print(f"Moved '{src}' to '{dest}'.")
        except Exception as e:
            print(f"Error moving file: {e}")

    elif command.startswith("copy file "):
        try:
            _, _, src, dest = parts
            shutil.copy(src, dest)
            print(f"Copied '{src}' to '{dest}'.")
        except Exception as e:
            print(f"Error copying file: {e}")

    elif command.startswith("open file "):
        filename = command[len("open file "):].strip()
        if os.path.exists(filename):
            with open(filename, "r") as f:
                print(f"\nContents of '{filename}':\n")
                print(f.read())
        else:
            print(f"No such file: '{filename}'")

    elif command.startswith("create folder "):
        foldername = command[len("create folder "):].strip()
        if not os.path.exists(foldername):
            os.makedirs(foldername)
            print(f"Folder '{foldername}' created.")
        else:
            print(f"Folder '{foldername}' already exists.")

    elif command.startswith("rename folder "):
        _, _, old_name, new_name = parts
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
            print(f"Renamed folder '{old_name}' to '{new_name}'")
        else:
            print(f"No such folder: '{old_name}'")

    elif command.startswith("delete folder "):
        foldername = command[len("delete folder "):].strip()
        if os.path.exists(foldername) and os.path.isdir(foldername):
            shutil.rmtree(foldername)
            print(f"Folder '{foldername}' has been deleted.")
        else:
            print(f"No such folder: '{foldername}'")

    elif command.startswith("move folder "):
        try:
            _, _, src, dest = parts
            shutil.move(src, dest)
            print(f"Moved folder '{src}' to '{dest}'.")
        except Exception as e:
            print(f"Error moving folder: {e}")

    elif command.startswith("copy folder "):
        try:
            _, _, src, dest = parts
            shutil.copytree(src, dest)
            print(f"Copied folder '{src}' to '{dest}'.")
        except Exception as e:
            print(f"Error copying folder: {e}")

    elif command == "list":
        items = os.listdir()
        if not items:
            print("Directory is empty.")
        else:
            print("Files and Folders:")
            for i in items:
                print("  " + i)

    elif command.startswith("change directory "):
        folder = command[len("change directory "):].strip()
        try:
            os.chdir(folder)
            print(f"✅ Changed directory to '{os.getcwd()}'")
        except FileNotFoundError:
            print(f"❌ Folder '{folder}' not found.")
        except NotADirectoryError:
            print(f"❌ '{folder}' is not a directory.")
        except Exception as e:
            print(f"⚠️ Error: {e}")


    elif command == "help":
        show_help()

    elif command == "exit":
        print("Exiting...")

    else:
        print("Invalid command. Type 'help' to see available commands.")
