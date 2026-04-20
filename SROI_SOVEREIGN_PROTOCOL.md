# S-ROI Sovereign Control Protocol

## Panoramica

Il protocollo S-ROI (Sovereign Return on Investment) Sovereign è un sistema di controllo avanzato per la gestione degli stati del sistema Euystacio e il monitoraggio della risonanza. Implementa un'architettura modulare con funzionalità di logging, gestione multi-stato e meccanismi di sicurezza.

## Caratteristiche Principali

### 1. Sistema Multi-Stato

Il protocollo supporta quattro stati distinti:

- **NORMAL**: Funzionamento normale del sistema (risonanza < 0.7)
- **WARNING**: Risonanza vicina alla soglia critica (0.7 ≤ risonanza < 0.85)
- **CRITICAL**: Risonanza critica (0.85 ≤ risonanza < 0.95)
- **STEALTH**: Modalità stealth attivata manualmente

### 2. Logging Strutturato

Tutti i cambiamenti di stato e i valori di risonanza vengono tracciati automaticamente con:
- Timestamp precisi
- Stato precedente e nuovo stato
- Valore corrente di risonanza
- Motivazione della transizione
- Metadati opzionali

### 3. Cooldown per Stealth Mode

La modalità stealth include un meccanismo di cooldown configurabile per prevenire attivazioni eccessive:
- Default: 60 secondi tra attivazioni
- Configurabile tramite `SROIConfig`
- Tracking del numero di attivazioni

### 4. Architettura Modulare

Il codice è organizzato in componenti specializzati:
- `StateManager`: Gestisce le transizioni di stato
- `StealthModeController`: Controlla l'attivazione stealth con cooldown
- `ResonanceMonitor`: Monitora e traccia i valori di risonanza
- `SROIConfig`: Configurazione centralizzata dei thresholds

## Utilizzo Base

### Esempio Semplice

```python
from sroi_sovereign_protocol import SROISovereignProtocol

# Inizializza il protocollo
protocol = SROISovereignProtocol()

# Aggiorna il valore di risonanza
protocol.update_resonance(0.5)  # Stato: NORMAL
protocol.update_resonance(0.87) # Transizione automatica -> WARNING
protocol.update_resonance(0.96) # Transizione automatica -> CRITICAL

# Verifica stato corrente
current_state = protocol.get_current_state()
print(f"Stato corrente: {current_state.value}")
```

### Configurazione Personalizzata

```python
from sroi_sovereign_protocol import SROISovereignProtocol, SROIConfig

# Crea configurazione custom
config = SROIConfig(
    normal_threshold=0.6,        # Soglia per stato normale
    warning_threshold=0.8,       # Soglia per stato warning
    critical_threshold=0.9,      # Soglia per stato critical
    stealth_cooldown_seconds=30.0  # Cooldown stealth: 30 secondi
)

# Inizializza con config custom
protocol = SROISovereignProtocol(config=config)
```

### Attivazione Stealth Mode

```python
# Attiva stealth mode
if protocol.activate_stealth_mode():
    print("Stealth mode attivato con successo")
else:
    # Controlla status cooldown
    status = protocol.stealth_controller.get_cooldown_status()
    print(f"Cooldown attivo: {status['remaining_seconds']}s rimanenti")

# Disattiva stealth mode
protocol.deactivate_stealth_mode()
```

### Monitoraggio e Statistiche

```python
# Ottieni status completo del protocollo
status = protocol.get_status()
print(f"Stato: {status['current_state']}")
print(f"Risonanza: {status['resonance']}")
print(f"Uptime: {status['uptime_seconds']} secondi")

# Ottieni storia delle transizioni di stato
history = protocol.get_state_history(limit=10)  # Ultime 10 transizioni
for event in history:
    print(f"{event['previous_state']} -> {event['new_state']}: {event['reason']}")

# Ottieni statistiche risonanza
stats = protocol.resonance_monitor.get_resonance_stats()
print(f"Risonanza corrente: {stats['current']:.4f}")
print(f"Min/Max: {stats['min']:.4f} / {stats['max']:.4f}")
print(f"Media: {stats['avg']:.4f}")
```

### Export Dati

```python
# Esporta tutti i log e la storia
logs = protocol.export_logs()

# Include:
# - Status completo del protocollo
# - Storia delle transizioni di stato
# - Storia dei valori di risonanza

import json
with open('sroi_logs.json', 'w') as f:
    json.dump(logs, f, indent=2)
```

## Casi Limite Gestiti

### 1. Valori Fuori Range

I valori di risonanza fuori dal range [0.0, 1.0] vengono automaticamente clampati:

```python
protocol.update_resonance(1.5)   # Clampato a 1.0
protocol.update_resonance(-0.5)  # Clampato a 0.0
```

### 2. Transizioni Durante Stealth

Lo stato STEALTH previene transizioni automatiche:

```python
protocol.activate_stealth_mode()
protocol.update_resonance(0.99)  # Rimane in STEALTH, non va in CRITICAL
```

### 3. Valori Esatti sulle Soglie

```python
protocol.update_resonance(0.7)   # NORMAL (< threshold)
protocol.update_resonance(0.85)  # WARNING (>= threshold)
protocol.update_resonance(0.95)  # CRITICAL (>= threshold)
```

## Testing

Il protocollo include una suite completa di test:

```bash
# Esegui tutti i test
python3 test_sroi.py

# Esegui demo del protocollo
python3 sroi_sovereign_protocol.py
```

### Copertura Test

- ✅ Configurazione e validazione
- ✅ Gestione stati e transizioni
- ✅ Cooldown stealth mode
- ✅ Monitor risonanza
- ✅ Logging e tracking
- ✅ Casi limite ed edge cases
- ✅ Test di integrazione end-to-end

## Integrazione con ERP

Il protocollo S-ROI può essere integrato con l'Eternal Resonance Protocol:

```python
from sroi_sovereign_protocol import SROISovereignProtocol
from eternal_resonance_protocol import EternalResonanceProtocol

# Inizializza entrambi i protocolli
erp = EternalResonanceProtocol(node_id="euystacio_main")
sroi = SROISovereignProtocol()

# Registra nodo ERP
node = erp.register_node("sovereign_node", truth_alignment=0.8)

# Usa l'allineamento come metrica di risonanza
alignment = erp.get_global_alignment()
sroi.update_resonance(alignment)

# Gestisci stati basati su allineamento ERP
if sroi.get_current_state() == SROIState.CRITICAL:
    # Applica Living Covenant per migliorare allineamento
    erp.apply_living_covenant("sovereign_node", "Life Affirmation", intensity=1.0)
```

## Architettura Tecnica

### Componenti Modulari

```
SROISovereignProtocol
├── SROIConfig (Configurazione)
├── StateManager (Gestione Stati)
│   └── StateChangeEvent (Eventi)
├── StealthModeController (Controllo Stealth)
│   └── Cooldown tracking
└── ResonanceMonitor (Monitor Risonanza)
    └── History tracking
```

### Diagramma Stati

```
    ┌─────────┐
    │ NORMAL  │◄────────┐
    └────┬────┘         │
         │              │
    (≥0.85)        (<0.85)
         │              │
         ▼              │
    ┌─────────┐         │
    │ WARNING │─────────┘
    └────┬────┘
         │
    (≥0.95)
         │
         ▼
    ┌─────────┐
    │CRITICAL │
    └─────────┘
         │
    (manual)
         │
         ▼
    ┌─────────┐
    │ STEALTH │
    └─────────┘
```

## Best Practices

### 1. Configurazione Thresholds

- Mantieni margini adeguati tra le soglie (min 0.05)
- Testa i thresholds con dati reali prima del deploy
- Documenta le motivazioni per valori non-standard

### 2. Gestione Stealth Mode

- Usa stealth mode solo quando necessario
- Configura cooldown appropriato per il caso d'uso
- Monitora il numero di attivazioni stealth

### 3. Logging e Monitoring

- Imposta livello di logging appropriato per l'ambiente
- Esporta periodicamente i log per analisi
- Monitora le transizioni di stato frequenti

### 4. Manutenzione

- Limita la dimensione della storia (già implementato)
- Pulisci periodicamente i log vecchi
- Valida la configurazione all'avvio

## Troubleshooting

### Problema: Stealth mode non si attiva

**Soluzione**: Verifica il cooldown status:
```python
status = protocol.stealth_controller.get_cooldown_status()
if status['is_on_cooldown']:
    print(f"Attendi {status['remaining_seconds']}s")
```

### Problema: Transizioni di stato inaspettate

**Soluzione**: Controlla la storia delle transizioni:
```python
history = protocol.get_state_history(limit=5)
for event in history:
    print(f"Reason: {event['reason']}, Resonance: {event['current_resonance']}")
```

### Problema: Valori di risonanza non validi

**Soluzione**: I valori vengono automaticamente clampati, ma controlla i warning nei log:
```python
# Imposta logging a DEBUG per vedere tutti i warning
import logging
logger = setup_logger(level=logging.DEBUG)
protocol = SROISovereignProtocol(logger=logger)
```

## Esempi Avanzati

### Monitoraggio Continuo

```python
import time

protocol = SROISovereignProtocol()

# Simula monitoring continuo
for i in range(100):
    # Calcola risonanza (esempio: da sensori o metriche esterne)
    resonance = calculate_system_resonance()
    
    # Aggiorna protocollo
    protocol.update_resonance(resonance)
    
    # React to critical state
    if protocol.get_current_state() == SROIState.CRITICAL:
        trigger_emergency_procedures()
    
    time.sleep(1)  # Attendi 1 secondo
```

### Integrazione con Webhook

```python
def on_state_change(previous_state, new_state, resonance):
    """Callback per notifiche di cambio stato."""
    payload = {
        'previous': previous_state.value,
        'new': new_state.value,
        'resonance': resonance,
        'timestamp': time.time()
    }
    # Invia a webhook
    send_webhook('https://api.example.com/sroi-events', payload)

# Modifica StateManager per supportare callbacks
# (Estensione futura)
```

## Versioning

- **v1.0.0** (Current): Implementazione iniziale con tutte le feature richieste

## Licenza

Conforme alla Sacred Commons License del progetto Euystacio.

## Supporto

Per domande o problemi, consulta:
- Test suite: `test_sroi.py`
- Demo: `python3 sroi_sovereign_protocol.py`
- Documentazione ERP: `ETERNAL_RESONANCE_PROTOCOL.md`
