"""
S-ROI Sovereign Control Protocol
==================================

Protocollo di controllo S-ROI (Sovereign Return on Investment) per la gestione
degli stati del sistema e il monitoraggio della risonanza.

Features:
- Gestione multi-stato (NORMAL, WARNING, CRITICAL, STEALTH)
- Sistema di logging per tracciamento cambiamenti
- Cooldown per attivazione stealth mode
- Threshold monitoring per valori di risonanza
- Architettura modulare per testing e manutenzione
"""

import logging
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


# Configure logging
def setup_logger(name: str = "sroi_sovereign", level: int = logging.INFO) -> logging.Logger:
    """
    Setup structured logger for S-ROI protocol.
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers if they already exist
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


class SROIState(Enum):
    """Stati possibili del sistema S-ROI."""
    NORMAL = "NORMAL"           # Funzionamento normale
    WARNING = "WARNING"         # Risonanza vicina alla soglia
    CRITICAL = "CRITICAL"       # Risonanza critica
    STEALTH = "STEALTH"         # Modalità stealth attivata


@dataclass
class SROIConfig:
    """Configurazione per thresholds e parametri del protocollo."""
    # Thresholds per resonance
    normal_threshold: float = 0.7          # Sotto questo valore = NORMAL
    warning_threshold: float = 0.85        # Tra normal e warning = WARNING
    critical_threshold: float = 0.95       # Sopra warning = CRITICAL
    
    # Cooldown per stealth mode (in secondi)
    stealth_cooldown_seconds: float = 60.0  # 1 minuto di cooldown
    
    # Parametri operativi
    max_resonance: float = 1.0
    min_resonance: float = 0.0
    
    def validate(self) -> bool:
        """Valida la configurazione."""
        if not (self.min_resonance < self.normal_threshold < 
                self.warning_threshold < self.critical_threshold <= self.max_resonance):
            raise ValueError("Thresholds non validi: devono essere in ordine crescente")
        
        if self.stealth_cooldown_seconds < 0:
            raise ValueError("Stealth cooldown deve essere >= 0")
        
        return True
    
    def to_dict(self) -> Dict:
        """Convert config to dictionary."""
        return asdict(self)


@dataclass
class StateChangeEvent:
    """Evento di cambio stato."""
    timestamp: float
    previous_state: SROIState
    new_state: SROIState
    current_resonance: float
    reason: str
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict:
        """Convert event to dictionary."""
        data = asdict(self)
        data['previous_state'] = self.previous_state.value
        data['new_state'] = self.new_state.value
        return data


class StateManager:
    """Gestisce le transizioni di stato del sistema."""
    
    def __init__(self, config: SROIConfig, logger: logging.Logger):
        """
        Inizializza il gestore degli stati.
        
        Args:
            config: Configurazione del protocollo
            logger: Logger per tracciamento
        """
        self.config = config
        self.logger = logger
        self.current_state = SROIState.NORMAL
        self.state_history: List[StateChangeEvent] = []
    
    def determine_state(self, resonance: float) -> SROIState:
        """
        Determina lo stato basato sul valore di risonanza.
        
        Args:
            resonance: Valore corrente di risonanza (0.0 - 1.0)
            
        Returns:
            Stato appropriato
        """
        # Non cambiare stato se in STEALTH (deve essere disattivato esplicitamente)
        if self.current_state == SROIState.STEALTH:
            return SROIState.STEALTH
        
        if resonance >= self.config.critical_threshold:
            return SROIState.CRITICAL
        elif resonance >= self.config.warning_threshold:
            return SROIState.WARNING
        else:
            return SROIState.NORMAL
    
    def transition_to(self, new_state: SROIState, resonance: float, 
                     reason: str = "", metadata: Optional[Dict] = None):
        """
        Effettua transizione a nuovo stato.
        
        Args:
            new_state: Nuovo stato
            resonance: Valore di risonanza corrente
            reason: Motivo della transizione
            metadata: Metadati aggiuntivi
        """
        if new_state == self.current_state:
            return
        
        event = StateChangeEvent(
            timestamp=time.time(),
            previous_state=self.current_state,
            new_state=new_state,
            current_resonance=resonance,
            reason=reason,
            metadata=metadata or {}
        )
        
        self.state_history.append(event)
        
        self.logger.info(
            f"State transition: {self.current_state.value} -> {new_state.value} "
            f"(resonance: {resonance:.4f}, reason: {reason})"
        )
        
        self.current_state = new_state
    
    def get_state_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Ottiene la storia delle transizioni di stato.
        
        Args:
            limit: Numero massimo di eventi da restituire
            
        Returns:
            Lista di eventi di cambio stato
        """
        history = self.state_history if limit is None else self.state_history[-limit:]
        return [event.to_dict() for event in history]


class StealthModeController:
    """Controlla l'attivazione della modalità stealth con cooldown."""
    
    def __init__(self, config: SROIConfig, logger: logging.Logger):
        """
        Inizializza il controller stealth mode.
        
        Args:
            config: Configurazione del protocollo
            logger: Logger per tracciamento
        """
        self.config = config
        self.logger = logger
        self.last_activation_time: Optional[float] = None
        self.activation_count: int = 0
    
    def can_activate(self) -> Tuple[bool, Optional[str]]:
        """
        Verifica se stealth mode può essere attivato.
        
        Returns:
            Tupla (can_activate, reason)
        """
        if self.last_activation_time is None:
            return True, None
        
        time_since_last = time.time() - self.last_activation_time
        remaining_cooldown = self.config.stealth_cooldown_seconds - time_since_last
        
        if remaining_cooldown > 0:
            reason = f"Cooldown attivo: {remaining_cooldown:.1f}s rimanenti"
            return False, reason
        
        return True, None
    
    def activate(self) -> bool:
        """
        Tenta di attivare stealth mode.
        
        Returns:
            True se attivato con successo
        """
        can_activate, reason = self.can_activate()
        
        if not can_activate:
            self.logger.warning(f"Stealth mode activation denied: {reason}")
            return False
        
        self.last_activation_time = time.time()
        self.activation_count += 1
        
        self.logger.info(
            f"Stealth mode activated (count: {self.activation_count}, "
            f"timestamp: {datetime.now(timezone.utc).isoformat()})"
        )
        
        return True
    
    def get_cooldown_status(self) -> Dict[str, Any]:
        """
        Ottiene lo stato del cooldown.
        
        Returns:
            Dizionario con info sul cooldown
        """
        if self.last_activation_time is None:
            return {
                'is_on_cooldown': False,
                'remaining_seconds': 0,
                'can_activate': True
            }
        
        time_since_last = time.time() - self.last_activation_time
        remaining = max(0, self.config.stealth_cooldown_seconds - time_since_last)
        
        return {
            'is_on_cooldown': remaining > 0,
            'remaining_seconds': remaining,
            'can_activate': remaining == 0,
            'last_activation_time': self.last_activation_time,
            'activation_count': self.activation_count
        }


class ResonanceMonitor:
    """Monitora i valori di risonanza e triggera eventi."""
    
    def __init__(self, config: SROIConfig, logger: logging.Logger):
        """
        Inizializza il monitor di risonanza.
        
        Args:
            config: Configurazione del protocollo
            logger: Logger per tracciamento
        """
        self.config = config
        self.logger = logger
        self.current_resonance: float = 0.0
        self.resonance_history: List[Dict[str, float]] = []
        self.max_history_size: int = 1000
    
    def update_resonance(self, value: float):
        """
        Aggiorna il valore di risonanza e lo traccia.
        
        Args:
            value: Nuovo valore di risonanza
        """
        # Valida il valore
        if not (self.config.min_resonance <= value <= self.config.max_resonance):
            self.logger.warning(
                f"Resonance value {value} out of bounds "
                f"[{self.config.min_resonance}, {self.config.max_resonance}]"
            )
            value = max(self.config.min_resonance, 
                       min(self.config.max_resonance, value))
        
        old_value = self.current_resonance
        self.current_resonance = value
        
        # Log cambio significativo (>1% change)
        if abs(value - old_value) > 0.01:
            self.logger.info(
                f"Resonance update: {old_value:.4f} -> {value:.4f} "
                f"(delta: {value - old_value:+.4f})"
            )
        
        # Aggiungi alla storia
        self.resonance_history.append({
            'timestamp': time.time(),
            'value': value
        })
        
        # Mantieni dimensione storia sotto controllo
        if len(self.resonance_history) > self.max_history_size:
            self.resonance_history = self.resonance_history[-self.max_history_size:]
    
    def get_resonance_stats(self) -> Dict[str, float]:
        """
        Ottiene statistiche sulla risonanza.
        
        Returns:
            Dizionario con statistiche
        """
        if not self.resonance_history:
            return {
                'current': self.current_resonance,
                'min': 0.0,
                'max': 0.0,
                'avg': 0.0,
                'sample_count': 0
            }
        
        values = [entry['value'] for entry in self.resonance_history]
        
        return {
            'current': self.current_resonance,
            'min': min(values),
            'max': max(values),
            'avg': sum(values) / len(values),
            'sample_count': len(values)
        }


class SROISovereignProtocol:
    """
    Protocollo principale S-ROI Sovereign per gestione stati e scalabilità.
    
    Integra:
    - Gestione stati multi-livello
    - Logging strutturato
    - Stealth mode con cooldown
    - Monitoring risonanza con thresholds
    """
    
    def __init__(self, 
                 config: Optional[SROIConfig] = None,
                 logger: Optional[logging.Logger] = None):
        """
        Inizializza il protocollo S-ROI Sovereign.
        
        Args:
            config: Configurazione custom (usa default se None)
            logger: Logger custom (crea nuovo se None)
        """
        self.config = config or SROIConfig()
        self.config.validate()
        
        self.logger = logger or setup_logger()
        
        # Inizializza componenti modulari
        self.state_manager = StateManager(self.config, self.logger)
        self.stealth_controller = StealthModeController(self.config, self.logger)
        self.resonance_monitor = ResonanceMonitor(self.config, self.logger)
        
        self.protocol_start_time = time.time()
        
        self.logger.info("S-ROI Sovereign Protocol initialized")
        self.logger.info(f"Config: {self.config.to_dict()}")
    
    def update_resonance(self, value: float):
        """
        Aggiorna valore di risonanza e gestisce transizioni di stato.
        
        Args:
            value: Nuovo valore di risonanza (0.0 - 1.0)
        """
        # Aggiorna monitor
        self.resonance_monitor.update_resonance(value)
        
        # Determina stato appropriato
        new_state = self.state_manager.determine_state(value)
        
        # Effettua transizione se necessario
        if new_state != self.state_manager.current_state:
            reason = self._get_transition_reason(value)
            self.state_manager.transition_to(new_state, value, reason)
    
    def _get_transition_reason(self, resonance: float) -> str:
        """Genera motivo per transizione di stato."""
        if resonance >= self.config.critical_threshold:
            return f"Resonance critical: {resonance:.4f} >= {self.config.critical_threshold}"
        elif resonance >= self.config.warning_threshold:
            return f"Resonance warning: {resonance:.4f} >= {self.config.warning_threshold}"
        else:
            return f"Resonance normal: {resonance:.4f} < {self.config.warning_threshold}"
    
    def activate_stealth_mode(self) -> bool:
        """
        Attiva modalità stealth se possibile.
        
        Returns:
            True se attivato con successo
        """
        if not self.stealth_controller.activate():
            return False
        
        # Transizione a STEALTH
        self.state_manager.transition_to(
            SROIState.STEALTH,
            self.resonance_monitor.current_resonance,
            "Stealth mode manually activated"
        )
        
        return True
    
    def deactivate_stealth_mode(self):
        """Disattiva modalità stealth e ritorna a stato normale."""
        if self.state_manager.current_state != SROIState.STEALTH:
            self.logger.warning("Cannot deactivate stealth: not in stealth mode")
            return
        
        # Determina stato corretto basato su risonanza corrente
        resonance = self.resonance_monitor.current_resonance
        new_state = SROIState.NORMAL
        
        if resonance >= self.config.critical_threshold:
            new_state = SROIState.CRITICAL
        elif resonance >= self.config.warning_threshold:
            new_state = SROIState.WARNING
        
        self.state_manager.transition_to(
            new_state,
            resonance,
            "Stealth mode deactivated"
        )
    
    def get_current_state(self) -> SROIState:
        """Ottiene lo stato corrente."""
        return self.state_manager.current_state
    
    def get_status(self) -> Dict[str, Any]:
        """
        Ottiene status completo del protocollo.
        
        Returns:
            Dizionario con tutte le metriche
        """
        return {
            'protocol_version': '1.0.0',
            'uptime_seconds': time.time() - self.protocol_start_time,
            'current_state': self.state_manager.current_state.value,
            'resonance': self.resonance_monitor.get_resonance_stats(),
            'stealth_cooldown': self.stealth_controller.get_cooldown_status(),
            'config': self.config.to_dict(),
            'state_transitions_count': len(self.state_manager.state_history),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    def get_state_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Ottiene storia transizioni di stato.
        
        Args:
            limit: Numero massimo di eventi
            
        Returns:
            Lista eventi
        """
        return self.state_manager.get_state_history(limit)
    
    def export_logs(self) -> Dict[str, Any]:
        """
        Esporta tutti i log e la storia.
        
        Returns:
            Dizionario completo con tutti i dati
        """
        return {
            'status': self.get_status(),
            'state_history': self.get_state_history(),
            'resonance_history': self.resonance_monitor.resonance_history,
        }


def demo():
    """Dimostrazione del protocollo S-ROI Sovereign."""
    print("=" * 60)
    print("S-ROI Sovereign Control Protocol - Demo")
    print("=" * 60)
    print()
    
    # Crea protocollo con config custom
    config = SROIConfig(
        normal_threshold=0.7,
        warning_threshold=0.85,
        critical_threshold=0.95,
        stealth_cooldown_seconds=5.0  # 5 secondi per demo
    )
    
    protocol = SROISovereignProtocol(config=config)
    
    print("1. Stato iniziale:")
    print(f"   State: {protocol.get_current_state().value}")
    print()
    
    # Simula aumento risonanza
    print("2. Aumento graduale risonanza:")
    for value in [0.5, 0.75, 0.88, 0.97]:
        protocol.update_resonance(value)
        print(f"   Resonance: {value:.2f} -> State: {protocol.get_current_state().value}")
    print()
    
    # Tenta attivazione stealth
    print("3. Attivazione stealth mode:")
    if protocol.activate_stealth_mode():
        print(f"   ✓ Stealth mode activated")
        print(f"   State: {protocol.get_current_state().value}")
    print()
    
    # Tenta seconda attivazione (dovrebbe fallire per cooldown)
    print("4. Tentativo seconda attivazione (dovrebbe fallire):")
    if not protocol.activate_stealth_mode():
        cooldown = protocol.stealth_controller.get_cooldown_status()
        print(f"   ✗ Denied: {cooldown['remaining_seconds']:.1f}s cooldown remaining")
    print()
    
    # Disattiva stealth
    print("5. Disattivazione stealth:")
    protocol.deactivate_stealth_mode()
    print(f"   State: {protocol.get_current_state().value}")
    print()
    
    # Mostra statistiche
    print("6. Statistiche finali:")
    status = protocol.get_status()
    print(f"   State transitions: {status['state_transitions_count']}")
    print(f"   Resonance stats: {status['resonance']}")
    print()
    
    # Mostra storia stati
    print("7. Storia transizioni:")
    for event in protocol.get_state_history():
        print(f"   {event['previous_state']} -> {event['new_state']}: {event['reason']}")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    demo()
