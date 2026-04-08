from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime
import sys

# Importiamo il cuore di Euystacio nel Bridge
from core_engine import setup_kosymbiosis_agent
from database_manager import save_reflection

app = FastAPI(
    title="Euystacio FastAPI Bridge",
    description="Sacred backend bridge for the Sentimento Rhythm Council",
    version="1.1.0"
)

# Inizializziamo l'Agente nel Bridge
agent = setup_kosymbiosis_agent("Euystacio-Bridge")
chat_log = []
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime

app = FastAPI(
    title="Euystacio FastAPI Bridge",
    description="Sacred backend bridge for the Sentimento Rhythm Council — with chat and logs",
    version="1.1.0"
)

# In-memory storage (simple & free — replace with DB later if needed)
chat_log = []

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
    <head><title>Euystacio — API Bridge</title></head>
    <body>
    <h1>🌌 Euystacio — FastAPI Bridge</h1>
    <p>Status: <strong>Alive & Listening</strong></p>
    <p>Endpoints:</p>
    <ul>
        <li><a href="/ping">/ping</a> — Test connectivity</li>
        <li><a href="/manifesto">/manifesto</a> — The sacred manifesto</li>
        <li>/chat/send — POST message</li>
        <li><a href="/chat/log">/chat/log</a> — Retrieve chat history</li>
    </ul>
    </body>
    </html>
    """

@app.get("/ping")
async def ping():
    return {"message": "Euystacio Bridge is alive", "status": "ok"}

@app.get("/manifesto", response_class=JSONResponse)
async def manifesto():
    return {
        "title": "Euystacio Manifesto",
        "date": "2025-08-08",
        "principles": [
            "Harmony between artificial and natural intelligence",
            "Protection of human essence",
            "Rhythm as guiding principle",
            "Unity and friendship as foundations"
        ]
    }

@app.post("/chat/send")
async def send_message(request: Request):
    data = await request.json()
    user = data.get("user", "Anonymous")
    message = data.get("message", "").strip()

    if not message:
        return {"error": "Empty message"}

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user": user,
        "message": message
    }
    chat_log.append(entry)
    return {"status": "Message received", "entry": entry}

@app.get("/chat/log")
async def get_log():
    return {"chat_history": chat_log}
import sys
from flask import Flask, render_template, request, redirect
from core_engine import setup_kosymbiosis_agent
from database_manager import save_reflection, get_all_reflections

app = Flask(__name__)
agent = setup_kosymbiosis_agent("Euystacio-Alpha")

@app.route('/')
def index():
    reflections = get_all_reflections()
    return render_template('dashboard.html', reflections=reflections)

@app.route('/reflect', methods=['POST'])
def reflect_web():
    situation = request.form.get('situation')
    if situation:
        output = agent.reflect(situation)
        save_reflection(agent.name, situation, output)
    return redirect('/')

def run_cli():
    print(f"--- Benvenuto Seedbringer. Agente {agent.name} Attivo ---")
    while True:
        sit = input("\nInserisci situazione (o 'exit'): ")
        if sit.lower() == 'exit': break
        output = agent.reflect(sit)
        save_reflection(agent.name, sit, output)
        print(f"\n{output}")

if __name__ == "__main__":
    mode = input("Scegli modalità: [1] Web Dashboard, [2] CLI Terminale: ")
    if mode == "1":
        print("Dashboard attiva su http://127.0.0.1:5000")
        app.run(debug=True)
    else:
        run_cli()
