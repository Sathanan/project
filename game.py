import tkinter as tk
import random
import time
import sqlite3
from datetime import datetime
from db import DB_PATH
from utils import format_time  # ✅ integriert

UFO_COUNT = 5

class Game:
    def __init__(self, root, username, return_to_menu):
        self.root = root
        self.username = username
        self.return_to_menu = return_to_menu
        self.ufo_buttons = []
        self.reaction_times = []
        self.ufo_number = 0
        self.start_time = 0
        self.session_id = None
        self.load_user_id()
        self.start_session()
        self.setup_game()

    def load_user_id(self):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE name = ?", (self.username,))
            self.user_id = c.fetchone()[0]

    def start_session(self):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            started = datetime.now().isoformat()
            c.execute("INSERT INTO sessions (user_id, started_at) VALUES (?, ?)", (self.user_id, started))
            self.session_id = c.lastrowid

    def setup_game(self):
        self.clear()
        self.ufo_label = tk.Label(self.root, text="Klicke auf die UFOs so schnell du kannst!")
        self.ufo_label.pack(pady=10)
        self.spawn_next_ufo()

    def spawn_next_ufo(self):
        if self.ufo_number >= UFO_COUNT:
            self.end_game()
            return

        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        x = random.randint(50, 300)
        y = random.randint(50, 300)
        self.ufo = tk.Button(self.root, text="🛸", command=self.hit_ufo)
        self.ufo.place(x=x, y=y)
        self.start_time = time.time()

    def hit_ufo(self):
        reaction_time = round(time.time() - self.start_time, 3)
        self.reaction_times.append(reaction_time)

        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO reactions (session_id, ufo_number, reaction_time) VALUES (?, ?, ?)",
                      (self.session_id, self.ufo_number + 1, reaction_time))

        self.ufo_number += 1
        self.spawn_next_ufo()

    def end_game(self):
        avg = round(sum(self.reaction_times) / len(self.reaction_times), 3)
        score = int((1 / avg) * 1000)

        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("UPDATE sessions SET avg_reaction = ? WHERE id = ?", (avg, self.session_id))
            c.execute("INSERT INTO scores (session_id, score) VALUES (?, ?)", (self.session_id, score))
            conn.commit()

        self.clear()
        tk.Label(self.root, text=f"🎯 Durchschnittliche Reaktionszeit: {avg} Sekunden").pack(pady=10)
        tk.Label(self.root, text=f"🏆 Dein Score: {score} Punkte").pack(pady=5)
        tk.Button(self.root, text="Replay", command=lambda: Game(self.root, self.username, self.return_to_menu)).pack()
        tk.Button(self.root, text="Zurück zum Menü", command=self.return_to_menu).pack()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def start_game(root, username, return_to_menu):
    Game(root, username, return_to_menu)