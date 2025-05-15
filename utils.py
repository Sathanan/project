import os
import csv
from db import DB_PATH
import sqlite3
from datetime import datetime

def ensure_data_dir():
    """Stellt sicher, dass der Datenordner existiert."""
    os.makedirs('data', exist_ok=True)

def format_time(seconds):
    """Formatiert eine Zeitdauer in Sekunden als mm:ss.SSS"""
    minutes = int(seconds // 60)
    remaining = seconds % 60
    return f"{minutes:02d}:{remaining:05.2f}"

def export_scores_to_csv(filename='data/scores_export.csv'):
    """Exportiert Score-Datenbankdaten in eine CSV-Datei."""
    ensure_data_dir()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            SELECT u.name, s.score, se.started_at, se.avg_reaction
            FROM users u
            JOIN sessions se ON u.id = se.user_id
            JOIN scores s ON s.session_id = se.id
            ORDER BY s.score DESC
        ''')
        data = c.fetchall()
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Score', 'Session Start', 'Avg Reaction'])
        writer.writerows(data)

    print(f"[✓] Scores wurden erfolgreich exportiert nach '{filename}'")

def get_current_timestamp():
    """Gibt den aktuellen Zeitstempel im ISO-Format zurück."""
    return datetime.now().isoformat()
