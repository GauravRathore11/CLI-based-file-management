import os
import shutil
import time

def show_help():
    help_text = (
        "\n👋 Welcome to Smart CLI!\n"
        "You can manage your files and folders using plain English.\n"
        "Here are some things you can ask me to do:\n\n"
        "  • Create a file called 'notes.txt'\n"
        "  • Delete the file 'old_report.pdf'\n"
        "  • Move 'file1.txt' to the 'Documents' folder\n"
        "  • Copy 'image.jpg' to 'Backup' folder\n"
        "  • Show all files in the current folder\n"
        "  • Create a new folder named 'Projects'\n"
        "  • Rename the folder 'New Folder' to '2025 Projects'\n"
        "  • Delete the folder called 'Temp'\n"
        "  • Rename the file 'draft.docx' to 'final.docx'\n"
        "  • Change directory to another folder\n\n"
        "Other commands:\n"
        "  help      → Show this help message\n"
        "  exit      → Exit Smart CLI\n"
    )
    return help_text

def handle_command(command):
    parts = command.split()
    if not parts:
        return "⚠️ Empty command."

    if command.startswith("search "):
        filename = command[len("search "):].strip()
        for root_dir, dirs, files in os.walk("."):
            if filename in files:
                return f"✅ Found '{filename}' in: {os.path.join(root_dir, filename)}"
        return f"❌ '{filename}' not found."

    elif command.startswith("create file "):
        filename = command[len("create file "):].strip()
        if os.path.exists(filename):
            return f"⚠️ '{filename}' already exists."
        open(filename, "w").close()
        return f"✅ '{filename}' has been created!"

    elif command.startswith("rename file "):
        if len(parts) < 4:
            return "⚠️ Please provide both old and new file names."
        _, _, old_name, new_name = parts
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
            return f"✅ Renamed '{old_name}' to '{new_name}'"
        return f"❌ No such file: '{old_name}'"
    
    elif command.startswith("file info "):
        filename = command[len("file info "):].strip()
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            file_type = os.path.splitext(filename)[1]
            last_modified = time.ctime(os.path.getmtime(filename))
            abs_path = os.path.abspath(filename)

            return (
                f"📄 File Info for '{filename}':\n"
                f"• Size: {file_size} bytes\n"
                f"• Type: {file_type or 'No Extension'}\n"
                f"• Last Modified: {last_modified}\n"
                f"• Absolute Path: {abs_path}"
            )
        else:
            return f"❌ File '{filename}' does not exist."

    elif command.startswith("delete file "):
        filename = command[len("delete file "):].strip()
        if os.path.exists(filename):
            os.remove(filename)
            return f"🗑️ '{filename}' has been deleted."
        return f"❌ No such file: '{filename}'"

    elif command.startswith("move file "):
        try:
            _, _, src, dest = parts
            shutil.move(src, dest)
            return f"📦 Moved '{src}' to '{dest}'."
        except Exception as e:
            return f"❌ Error moving file: {e}"

    elif command.startswith("copy file "):
        try:
            _, _, src, dest = parts
            shutil.copy(src, dest)
            return f"📄 Copied '{src}' to '{dest}'."
        except Exception as e:
            return f"❌ Error copying file: {e}"

    elif command.startswith("open file "):
        filename = command[len("open file "):].strip()
        if os.path.exists(filename):
            with open(filename, "r") as f:
                content = f.read()
            return f"📂 Content of '{filename}':\n\n{content}"
        return f"❌ No such file: '{filename}'"
    
    elif command.startswith("compress folder "):
        folder_path = command[len("compress folder "):].strip()
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            output_zip = folder_path.rstrip("/\\") + ".zip"
            try:
                shutil.make_archive(folder_path, 'zip', folder_path)
                return f"✅ Folder '{folder_path}' compressed to '{output_zip}'"
            except Exception as e:
                return f"❌ Compression failed: {e}"
        return f"❌ Folder '{folder_path}' does not exist"

    elif command.startswith("create folder "):
        foldername = command[len("create folder "):].strip()
        if not os.path.exists(foldername):
            os.makedirs(foldername)
            return f"📁 Folder '{foldername}' created."
        return f"⚠️ Folder '{foldername}' already exists."

    elif command.startswith("rename folder "):
        if len(parts) < 4:
            return "⚠️ Please provide both old and new folder names."
        _, _, old_name, new_name = parts
        if os.path.exists(old_name):
            os.rename(old_name, new_name)
            return f"✅ Renamed folder '{old_name}' to '{new_name}'"
        return f"❌ No such folder: '{old_name}'"

    elif command.startswith("delete folder "):
        foldername = command[len("delete folder "):].strip()
        if os.path.isdir(foldername):
            shutil.rmtree(foldername)
            return f"🗑️ Folder '{foldername}' has been deleted."
        return f"❌ No such folder: '{foldername}'"

    elif command.startswith("move folder "):
        try:
            _, _, src, dest = parts
            shutil.move(src, dest)
            return f"📦 Moved folder '{src}' to '{dest}'."
        except Exception as e:
            return f"❌ Error moving folder: {e}"

    elif command.startswith("copy folder "):
        try:
            _, _, src, dest = parts
            shutil.copytree(src, dest)
            return f"📁 Copied folder '{src}' to '{dest}'."
        except Exception as e:
            return f"❌ Error copying folder: {e}"

    elif command == "list":
        items = os.listdir()
        if not items:
            return "📂 Directory is empty."
        return "📁 Files and Folders:\n" + "\n".join(f"  • {item}" for item in items)

    elif command.startswith("change directory "):
        folder = command[len("change directory "):].strip()
        try:
            os.chdir(folder)
            return f"✅ Changed directory to '{os.getcwd()}'"
        except FileNotFoundError:
            return f"❌ Folder '{folder}' not found."
        except NotADirectoryError:
            return f"❌ '{folder}' is not a directory."
        except Exception as e:
            return f"⚠️ Error: {e}"

    elif command == "help":
        return show_help()

    elif command == "exit":
        return "Exiting..."

    return "❓ Invalid command. Type 'help' to see available commands."
