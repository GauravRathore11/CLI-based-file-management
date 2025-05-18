import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.ai_utils import get_command_from_natural_language
from app.commands import handle_command

def process_input():
    user_input = input_box.get()
    if user_input.lower() == "exit":
        chat_box.insert(tk.END, "Exiting...\n", "exit")
        chat_box.see(tk.END)
        root.quit()
        return

    chat_box.insert(tk.END, f"You: {user_input}\n", "user")
    chat_box.see(tk.END)

    command = get_command_from_natural_language(user_input)

    if command == "invalid":
        response = "😕 Sorry, I didn't understand that."
    else:
        response = handle_command(command)

    chat_box.insert(tk.END, f"Bot: {response}\n{'='*40}\n", "bot")
    chat_box.see(tk.END)
    input_box.delete(0, tk.END)

    selected_item = tree.focus()
    if selected_item:
        path = get_full_path(selected_item)
        parent_item = tree.parent(selected_item) if os.path.isfile(path) else selected_item
        refresh_node(parent_item)

def load_directory_tree(parent, path):
    try:
        for item in sorted(os.listdir(path), key=str.lower):
            abs_path = os.path.join(path, item)
            node = tree.insert(parent, "end", text=item, values=[abs_path], open=False)
            if os.path.isdir(abs_path):
                tree.insert(node, "end")  # Dummy to make expandable
    except PermissionError:
        pass

def on_tree_expand(event):
    item = tree.focus()
    path = tree.item(item, "values")[0]
    if tree.get_children(item):
        if tree.item(tree.get_children(item)[0], "text") == "":
            tree.delete(tree.get_children(item)[0])
            load_directory_tree(item, path)

def get_full_path(item):
    return tree.item(item, "values")[0]

def on_tree_select(event):
    selected_item = tree.focus()
    path = get_full_path(selected_item)
    if os.path.isfile(path):
        size = os.path.getsize(path)
        info = f"📄 File: {os.path.basename(path)}\nPath: {path}\nSize: {size} bytes"
        messagebox.showinfo("File Info", info)

def refresh_node(item):
    path = get_full_path(item)
    tree.delete(*tree.get_children(item))
    load_directory_tree(item, path)

def show_context_menu(event):
    selected_item = tree.identify_row(event.y)
    if selected_item:
        tree.selection_set(selected_item)
        context_menu.tk_popup(event.x_root, event.y_root)

def delete_item():
    item = tree.focus()
    path = get_full_path(item)
    try:
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.remove(path)
        tree.delete(item)
        chat_box.insert(tk.END, f"Bot: Deleted {path}\n{'='*40}\n", "bot")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def setup_theme():
    root.configure(bg="#121212")
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Treeview", 
                  background="#1e1e1e", 
                  foreground="#ffffff", 
                  fieldbackground="#1e1e1e",
                  rowheight=25)
    style.configure("TFrame", background="#121212")
    style.configure("TNotebook", background="#121212")
    style.configure("TNotebook.Tab", 
                  background="#333333", 
                  foreground="white",
                  padding=[10, 5])
    style.map("TNotebook.Tab", 
             background=[("selected", "#6a0dad")],
             foreground=[("selected", "white")])

    chat_box.configure(bg="#1e1e1e", fg="white", insertbackground="white")
    input_box.configure(bg="#1e1e1e", fg="white", insertbackground="white")
    send_button.configure(bg="#6a0dad", fg="white", activebackground="#800080", activeforeground="white")

    chat_box.tag_config("user", foreground="#00ff00")
    chat_box.tag_config("bot", foreground="#ff4444")
    chat_box.tag_config("exit", foreground="white")

def update_stats():
    try:
        cpu_usage = psutil.cpu_percent()
        mem_info = psutil.virtual_memory().percent

        # Clear and update CPU chart
        cpu_chart.clear()
        cpu_chart.bar(['CPU'], [cpu_usage], color='lime')
        cpu_chart.set_ylim(0, 100)
        cpu_chart.set_title('CPU Usage', color='white')
        cpu_chart.set_facecolor('#121212')
        cpu_chart.grid(True, color='gray', alpha=0.3)
        
        # Clear and update Memory chart
        mem_chart.clear()
        mem_chart.bar(['Memory'], [mem_info], color='cyan')
        mem_chart.set_ylim(0, 100)
        mem_chart.set_title('Memory Usage', color='white')
        mem_chart.set_facecolor('#121212')
        mem_chart.grid(True, color='gray', alpha=0.3)

        # Redraw canvases
        canvas_cpu.draw()
        canvas_mem.draw()
        
    except Exception as e:
        print(f"Error updating stats: {e}")
    
    root.after(1000, update_stats)

# Main GUI Setup
root = tk.Tk()
root.title("Smart CLI File Manager")
root.geometry("1200x700")

# Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# File Manager Tab
main_frame = ttk.Frame(notebook)
notebook.add(main_frame, text="File Manager")

# Treeview for directory structure
tree_frame = ttk.Frame(main_frame)
tree_frame.pack(side="left", fill="y", padx=10, pady=10)

tree = ttk.Treeview(tree_frame)
tree.pack(fill="both", expand=True)

# Initialize with current directory
root_path = "."
root_node = tree.insert("", "end", text=root_path, values=[root_path], open=True)
load_directory_tree(root_node, root_path)

# Bind events
tree.bind("<<TreeviewOpen>>", on_tree_expand)
tree.bind("<<TreeviewSelect>>", on_tree_select)
tree.bind("<Button-3>", show_context_menu)

# Chat interface
chat_frame = ttk.Frame(main_frame)
chat_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

chat_box = scrolledtext.ScrolledText(chat_frame, width=70, height=20, wrap=tk.WORD)
chat_box.pack(fill="both", expand=True)

input_frame = ttk.Frame(chat_frame)
input_frame.pack(fill="x", pady=(0, 10))

input_box = tk.Entry(input_frame, width=70)
input_box.pack(side="left", fill="x", expand=True, padx=(0, 5))
input_box.bind("<Return>", lambda event: process_input())

send_button = tk.Button(input_frame, text="Send", command=process_input)
send_button.pack(side="left")

# Context menu
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Delete", command=delete_item)

# System Stats Tab
stats_frame = ttk.Frame(notebook)
notebook.add(stats_frame, text="System Stats")

# Stats container
stats_container = ttk.Frame(stats_frame)
stats_container.pack(fill="both", expand=True, padx=10, pady=10)

# CPU Chart
fig_cpu = plt.Figure(figsize=(5, 3), facecolor='#121212')
cpu_chart = fig_cpu.add_subplot(111)
cpu_chart.set_facecolor('#121212')
cpu_chart.tick_params(colors='white')
for spine in cpu_chart.spines.values():
    spine.set_color('white')
canvas_cpu = FigureCanvasTkAgg(fig_cpu, master=stats_container)
canvas_cpu.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5)

# Memory Chart
fig_mem = plt.Figure(figsize=(5, 3), facecolor='#121212')
mem_chart = fig_mem.add_subplot(111)
mem_chart.set_facecolor('#121212')
mem_chart.tick_params(colors='white')
for spine in mem_chart.spines.values():
    spine.set_color('white')
canvas_mem = FigureCanvasTkAgg(fig_mem, master=stats_container)
canvas_mem.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5)

# Initialize theme and start stats update
setup_theme()
update_stats()

root.mainloop()