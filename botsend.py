import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import discord
import asyncio
import threading
import os
import sys
import traceback

def log_exceptions(type, value, tb):
    with open("error_log.txt", "w") as f:
        traceback.print_exception(type, value, tb, file=f)

sys.excepthook = log_exceptions

# ---- Discord bot client setup ----
class BotClient(discord.Client):
    def __init__(self, token, channel_id, message, file_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.channel_id = int(channel_id)
        self.message = message
        self.file_path = file_path

    async def on_ready(self):
        try:
            channel = self.get_channel(self.channel_id)
            if not channel:
                raise Exception("Channel not found.")
            file = discord.File(self.file_path) if self.file_path else None
            await channel.send(content=self.message if self.message else None, file=file if file else None)
            messagebox.showinfo("Success", "Message sent!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        await self.close()

    def run_bot(self):
        try:
            self.run(self.token)
        except discord.LoginFailure:
            messagebox.showerror("Error", "Invalid token.")

# ---- GUI setup ----
class BotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Bot Messenger")
        self.root.geometry("500x400")
        self.root.configure(bg="#2e2e2e")
        self.main_frame = tk.Frame(self.root, bg="#2e2e2e")
        self.main_frame.pack(expand=True)

        self.token_var = tk.StringVar()
        self.channel_var = tk.StringVar()
        self.message_var = tk.StringVar()
        self.file_path = ""

        self.build_gui()


    def build_gui(self):
        fields = [
            ("Bot Token:", self.token_var),
            ("Channel ID:", self.channel_var),
            ("Message:", self.message_var),
        ]

        for i, (label_text, var) in enumerate(fields):
            label = tk.Label(self.main_frame, text=label_text, bg="#2e2e2e", fg="white", font=("Arial", 10))
            entry = tk.Entry(self.main_frame, textvariable=var, width=40, bg="#1e1e1e", fg="white", insertbackground="white")
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry.grid(row=i, column=1, padx=10, pady=5)

        file_button = tk.Button(self.main_frame, text="Select File", command=self.select_file)
        file_button.grid(row=len(fields), column=1, sticky="w", padx=10, pady=10)

        send_button = tk.Button(self.main_frame, text="Send Message", command=self.send_message)
        send_button.grid(row=len(fields) + 1, column=1, sticky="w", padx=10)

    def select_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.file_path = path
            messagebox.showinfo("File Selected", os.path.basename(path))

    def send_message(self):
        token = self.token_var.get().strip()
        channel_id = self.channel_var.get().strip()
        message = self.message_var.get().strip()

        if not token or not channel_id:
            messagebox.showwarning("Missing Info", "Token and Channel ID are required.")
            return

        client = BotClient(token, channel_id, message, self.file_path, intents=discord.Intents.default())
        threading.Thread(target=client.run_bot).start()

# ---- Main ----
if __name__ == "__main__":
    root = tk.Tk()
    app = BotGUI(root)
    root.mainloop()