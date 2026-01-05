import random
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip  # install with pip install pyperclip

# ---------------- Functions ----------------
def generate_password():
    try:
        length = int(length_entry.get())
        if length < 4:
            messagebox.showwarning("Warning", "Password length should be at least 4")
            return
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number for length")
        return

    char_pool = ""
    if upper_var.get():
        char_pool += string.ascii_uppercase
    if lower_var.get():
        char_pool += string.ascii_lowercase
    if digits_var.get():
        char_pool += string.digits
    if symbols_var.get():
        char_pool += string.punctuation

    if not char_pool:
        messagebox.showwarning("Warning", "Select at least one character type")
        return

    password = ''.join(random.choice(char_pool) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def copy_password():
    pwd = password_entry.get()
    if pwd:
        pyperclip.copy(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard")
    else:
        messagebox.showwarning("Warning", "No password to copy")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x300")
root.resizable(False, False)

# Title
tk.Label(root, text="Password Generator", font=("Arial", 16, "bold")).pack(pady=10)

# Frame for options
frame = tk.Frame(root)
frame.pack(pady=5)

tk.Label(frame, text="Password Length:").grid(row=0, column=0, sticky="w")
length_entry = tk.Entry(frame, width=5)
length_entry.grid(row=0, column=1, padx=5)
length_entry.insert(0, "12")  # default length

# Checkboxes
upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(frame, text="Uppercase", variable=upper_var).grid(row=1, column=0, sticky="w")
tk.Checkbutton(frame, text="Lowercase", variable=lower_var).grid(row=1, column=1, sticky="w")
tk.Checkbutton(frame, text="Numbers", variable=digits_var).grid(row=2, column=0, sticky="w")
tk.Checkbutton(frame, text="Symbols", variable=symbols_var).grid(row=2, column=1, sticky="w")

# Generate button
tk.Button(root, text="Generate Password", command=generate_password, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

# Password display
password_entry = tk.Entry(root, width=30, font=("Arial", 12))
password_entry.pack(pady=5)

# Copy button
tk.Button(root, text="Copy Password", command=copy_password, bg="#2196F3", fg="white", font=("Arial", 12, "bold")).pack(pady=5)

# Run GUI
root.mainloop()
