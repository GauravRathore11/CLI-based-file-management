import tkinter as tk
from app.commands import handle_command, show_help

class CLIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My CLI File Manager")
        self.root.geometry("700x400")
        
        self.output = tk.Text(root, wrap=tk.WORD, bg="black", fg="lime", insertbackground="lime")
        self.output.pack(fill=tk.BOTH, expand=True)
        
        self.entry = tk.Entry(root, bg="black", fg="white", insertbackground="white")
        self.entry.pack(fill=tk.X)
        self.entry.bind("<Return>", self.process_command)

        self.output.insert(tk.END, "Welcome to CLI File Manager!\n\n")
        self.output.insert(tk.END, "Type commands like: create file test.txt, delete file test.txt, list, exit\n\n")
        self.output.insert(tk.END, "="*60 + "\n")
    
    def process_command(self, event):
        cmd = self.entry.get().strip().lower()
        self.output.insert(tk.END, f">>> {cmd}\n")
        if cmd == "exit":
            self.root.quit()
        else:
            from io import StringIO
            import sys
            old_stdout = sys.stdout
            sys.stdout = buffer = StringIO()
            try:
                handle_command(cmd)
            except Exception as e:
                print(f"Error: {e}")
            sys.stdout = old_stdout
            self.output.insert(tk.END, buffer.getvalue())
        self.output.insert(tk.END, "="*60 + "\n")
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CLIApp(root)
    root.mainloop()
