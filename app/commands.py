import os

def show_help():
    print("\nAvailable commands:")
    print("create file <filename>")
    print("delete file <filename>")
    print("list")
    print("exit\n")

print("Welcome to CLI File Manager!")
show_help()

while True:
    command = input(">>> ").strip().lower()

    if command.startswith("create file "):
        filename = command[len("create file "):].strip()
        if os.path.exists(filename):
            print(f"'{filename}' already exists.")
        else:
            with open(filename, "w") as f:
                f.write("")
            print(f"'{filename}' has been created!")

    elif command.startswith("delete file "):
        filename = command[len("delete file "):].strip()
        if os.path.exists(filename):
            os.remove(filename)
            print(f"'{filename}' has been deleted.")
        else:
            print(f"No such file: '{filename}'")

    elif command == "list":
        files = os.listdir()
        if not files:
            print("Directory is empty.")
        else:
            print("Files and folders in current directory:")
            for f in files:
                print("  " + f)

    elif command == "exit":
        print("Exiting...")
        break

    else:
        print("Invalid command.")
        show_help()

    print("\n==========================================================")
