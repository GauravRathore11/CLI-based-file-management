import os
import shutil

def show_help():
    print("\nAvailable Commands:")
    print("  create file <filename>        → Create a new empty file")
    print("  delete file <filename>        → Delete a file")
    print("  move file <src> <dest>        → Move file from src to dest")
    print("  copy file <src> <dest>        → Copy file from src to dest")
    print("  search file <filename>        → Search for a file in current and subdirectories")
    print("  list                          → List all files and folders in current directory")
    print("  help                          → Show this help message")
    print("  exit                          → Exit the application\n")

def handle_command(command):
    if command.startswith("create file "):
        filename = command[len("create file "):].strip()
        if os.path.exists(filename):
            print(f"'{filename}' already exists.")
        else:
            open(filename, "w").close()
            print(f"'{filename}' has been created!")

    elif command.startswith("delete file "):
        filename = command[len("delete file "):].strip()
        if os.path.exists(filename):
            os.remove(filename)
            print(f"'{filename}' has been deleted.")
        else:
            print(f"No such file: '{filename}'")

    elif command.startswith("move file "):
        parts = command.split(maxsplit=3)
        if len(parts) == 4:
            src, dest = parts[2], parts[3]
            try:
                shutil.move(src, dest)
                print(f"Moved '{src}' to '{dest}'.")
            except Exception as e:
                print(f"Error moving file: {e}")
        else:
            print("Invalid move command. Usage: move file <src> <dest>")

    elif command.startswith("copy file "):
        parts = command.split(maxsplit=3)
        if len(parts) == 4:
            src, dest = parts[2], parts[3]
            try:
                shutil.copy(src, dest)
                print(f"Copied '{src}' to '{dest}'.")
            except Exception as e:
                print(f"Error copying file: {e}")
        else:
            print("Invalid copy command. Usage: copy file <src> <dest>")

    elif command.startswith("search file "):
        filename = command[len("search file "):].strip()
        found = False
        for root, dirs, files in os.walk("."):
            if filename in files:
                print(f"Found '{filename}' in: {os.path.join(root, filename)}")
                found = True
        if not found:
            print(f"'{filename}' not found.")

    elif command == "list":
        items = os.listdir()
        if not items:
            print("Directory is empty.")
        else:
            print("Files and Folders:")
            for i in items:
                print("  " + i)

    elif command == "help":
        show_help()

    elif command == "exit":
        print("Exiting...")

    else:
        print("Invalid command. Type 'help' to see available commands.")
