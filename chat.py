import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import random
import threading
import time

# ---------------- Chatbot Responses ----------------
responses = {
    "hello": ["Hello!", "Hi there!", "Hey! How are you?"],
    "how are you": ["I'm good, thank you!", "Doing well, and you?", "I am fine!"],
    "bye": ["Goodbye!", "See you later!", "Bye! Have a nice day!"],
    "name": ["Nice to meet you, {name}!", "Great to chat with you, {name}!"],
    "default": ["Sorry, I didn't understand that.", "Can you say that again?", "Hmm... interesting."]
}

user_name = ""

# ---------------- Text-to-Speech ----------------
def speak(text):
    def run():
        engine = pyttsx3.init()  # new engine each time
        engine.setProperty("rate", 150)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    threading.Thread(target=run).start()

# ---------------- Chatbot Logic ----------------
def get_response(msg):
    global user_name
    msg = msg.lower()

    # Name recognition
    if "my name is" in msg:
        user_name = msg.split("my name is")[-1].strip().title()
        return f"Nice to meet you, {user_name}!"
    
    for key in responses.keys():
        if key in msg:
            resp = random.choice(responses[key])
            if "{name}" in resp:
                resp = resp.format(name=user_name if user_name else "friend")
            return resp
    return random.choice(responses["default"])

# ---------------- GUI ----------------
def send_message():
    msg = user_entry.get().strip()
    if msg == "":
        return

    # Display user message
    chat_window.config(state='normal')
    chat_window.insert(tk.END, f"You: {msg}\n", "user")
    chat_window.config(state='disabled')
    chat_window.yview(tk.END)

    user_entry.delete(0, tk.END)

    # Simulate typing delay
    chat_window.config(state='normal')
    chat_window.insert(tk.END, "Bot: typing...\n", "bot_typing")
    chat_window.config(state='disabled')
    chat_window.yview(tk.END)
    root.update()

    time.sleep(0.8)  # Typing effect

    # Remove typing placeholder
    chat_window.config(state='normal')
    chat_window.delete("end-2l", "end-1l")
    chat_window.config(state='disabled')

    # Get bot reply
    reply = get_response(msg)
    chat_window.config(state='normal')
    chat_window.insert(tk.END, f"Bot: {reply}\n\n", "bot")
    chat_window.config(state='disabled')
    chat_window.yview(tk.END)

    speak(reply)  # Voice

# ---------------- Tkinter Window ----------------
root = tk.Tk()
root.title("Polished Chatbot with Voice")
root.geometry("450x550")
root.resizable(False, False)
root.configure(bg="#f2f2f2")

# Chat window
chat_window = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD, font=("Arial", 12))
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Tag styles for chat bubbles
chat_window.tag_configure("user", foreground="white", background="#4CAF50", lmargin1=5, lmargin2=5, rmargin=5)
chat_window.tag_configure("bot", foreground="white", background="#2196F3", lmargin1=5, lmargin2=5, rmargin=5)
chat_window.tag_configure("bot_typing", foreground="gray", background="#cccccc", lmargin1=5, lmargin2=5, rmargin=5)

# Entry & send button
frame = tk.Frame(root, bg="#f2f2f2")
frame.pack(pady=5)

user_entry = tk.Entry(frame, width=30, font=("Arial", 12))
user_entry.pack(side=tk.LEFT, padx=5)

send_button = tk.Button(frame, text="Send", command=send_message, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
send_button.pack(side=tk.LEFT)

root.bind('<Return>', lambda event=None: send_message())

root.mainloop()
