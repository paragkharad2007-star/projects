import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "tasks.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

# Save tasks to file
def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file)

# Add task
def add_task():
    task = entry.get().strip()
    if task:
        tasks.append({"title": task, "done": False})
        update_list()
        save_tasks()
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty")

# Mark task as done
def mark_done():
    try:
        index = listbox.curselection()[0]
        tasks[index]["done"] = True
        update_list()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task first")

# Delete task
def delete_task():
    try:
        index = listbox.curselection()[0]
        tasks.pop(index)
        update_list()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task first")

# Update task list
def update_list():
    listbox.delete(0, tk.END)
    for task in tasks:
        status = "✔" if task["done"] else "✖"
        listbox.insert(tk.END, f"[{status}] {task['title']}")

# GUI Window
root = tk.Tk()
root.title("To-Do List")
root.geometry("400x450")
root.resizable(False, False)

tasks = load_tasks()

# UI Elements
title = tk.Label(root, text="To-Do List", font=("Arial", 18, "bold"))
title.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 12))
entry.pack(pady=10, padx=20, fill=tk.X)

add_btn = tk.Button(root, text="Add Task", command=add_task)
add_btn.pack(pady=5)

listbox = tk.Listbox(root, font=("Arial", 12), height=10)
listbox.pack(pady=10, padx=20, fill=tk.BOTH)

done_btn = tk.Button(root, text="Mark as Done", command=mark_done)
done_btn.pack(pady=5)

delete_btn = tk.Button(root, text="Delete Task", command=delete_task)
delete_btn.pack(pady=5)

update_list()
root.mainloop()
