import json
import os

DB_FILE = "reflections_db.json"

def save_reflection(agent_name, situation, reflection_text):
    data = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    
    entry = {
        "agent": agent_name,
        "situation": situation,
        "reflection": reflection_text,
        "timestamp": reflection_text.split('\n')[0] # Estrae il timestamp dal testo generato
    }
    data.append(entry)
    
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_all_reflections():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
