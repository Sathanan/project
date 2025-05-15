import sqlite3
from tkinter import messagebox
from db import DB_PATH

def show_scoreboard():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''SELECT u.name, MAX(s.score) FROM users u
                     JOIN sessions se ON u.id = se.user_id
                     JOIN scores s ON s.session_id = se.id
                     GROUP BY u.id ORDER BY MAX(s.score) DESC LIMIT 10''')
        result = c.fetchall()
        scores = "\n".join([f"{i+1}. {r[0]} - {r[1]} Punkte" for i, r in enumerate(result)])
        messagebox.showinfo("Scoreboard", scores or "Keine Scores gefunden.")

def show_stats(username):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE name = ?", (username,))
        user_id = c.fetchone()[0]
        c.execute("SELECT COUNT(*), AVG(avg_reaction) FROM sessions WHERE user_id = ?", (user_id,))
        games, avg_reaction = c.fetchone()
        msg = f"Spiele insgesamt: {games}\nDurchschnittliche Reaktionszeit: {round(avg_reaction, 3) if avg_reaction else 0}s"
        messagebox.showinfo("Deine Statistiken", msg)