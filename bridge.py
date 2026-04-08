<script>
    const API_BASE = "TUO_URL_BACKEND"; // Inserisci qui l'URL del backend FastAPI

    // 1. Funzione per la Chat del Council (Nexus Logs)
    async function sendMessage() {
        const input = document.getElementById('chatInput');
        const log = document.getElementById('chat-log');
        const userMsg = input.value.trim();
        
        if(!userMsg) return;

        log.innerHTML += `<div class="text-white">> User: ${userMsg}</div>`;
        input.value = '';

        try {
            const response = await fetch(`${API_BASE}/chat/send`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user: "Seedbringer", message: userMsg })
            });
            const data = await response.json();
            log.innerHTML += `<div class="text-success">> System: Message Anchored in Audit Trail.</div>`;
        } catch (error) {
            log.innerHTML += `<div class="text-danger">> Error: Bridge Offline. Check Backend.</div>`;
        }
        log.scrollTop = log.scrollHeight;
    }

    // 2. Funzione per la Riflessione Euystacio (Lex Amoris)
    async function sendToBridge() {
        const input = document.getElementById('situationInput');
        const log = document.getElementById('chat-log');
        const situation = input.value.trim();

        if(!situation) return;

        log.innerHTML += `<div class="text-warning">> [APE] Processing Reflection for: "${situation.substring(0,20)}..."</div>`;
        
        try {
            // Chiamata all'agente Euystacio integrato nel bridge
            const response = await fetch(`${API_BASE}/chat/reflect`, { // Endpoint che abbiamo creato prima
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: situation })
            });
            const data = await response.json();
            
            // Visualizzazione della guida sacra
            log.innerHTML += `<div class="p-2 border border-success my-2" style="font-size:0.8rem;">${data.entry.sacred_guidance.replace(/\n/g, '<br>')}</div>`;
            input.value = '';
        } catch (error) {
            log.innerHTML += `<div class="text-danger">> Error: Euystacio Agent not responding.</div>`;
        }
        log.scrollTop = log.scrollHeight;
    }

    // Listener per il tasto invio
    document.getElementById('chatInput').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') sendMessage();
    });
</script>
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://euystaciocore.netlify.app"], # Il tuo indirizzo Netlify
    allow_methods=["*"],
    allow_headers=["*"],
)
