import tkinter as tk
from tkinter import messagebox
from db import init_db, get_or_create_user
from game import start_game
from stats import show_scoreboard, show_stats

class ReactionGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reaction Game")
        self.username = None
        init_db()
        self.show_intro()

    def show_intro(self):
        self.clear()
        tk.Label(self.root, text="Willkommen beim Reaction Game!").pack(pady=10)
        tk.Label(self.root, text="Bitte Namen eingeben:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
        tk.Button(self.root, text="Weiter", command=self.save_user).pack(pady=5)

    def save_user(self):
        name = self.name_entry.get().strip()
        if name:
            self.username = name
            get_or_create_user(name)
            self.show_menu()
        else:
            messagebox.showerror("Fehler", "Name darf nicht leer sein")

    def show_menu(self):
        self.clear()
        tk.Label(self.root, text=f"Hallo, {self.username}!").pack(pady=10)
        tk.Button(self.root, text="Spiel starten", command=lambda: start_game(self.root, self.username, self.show_menu)).pack(fill='x')
        tk.Button(self.root, text="Bedienungsanleitung", command=self.show_instructions).pack(fill='x')
        tk.Button(self.root, text="Scoreboard", command=show_scoreboard).pack(fill='x')
        tk.Button(self.root, text="Statistiken", command=lambda: show_stats(self.username)).pack(fill='x')
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(fill='x')

    def show_instructions(self):
        messagebox.showinfo("Anleitung", "Klicke so schnell wie möglich auf die UFOs!")

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = ReactionGameApp(root)
    root.mainloop()