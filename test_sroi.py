#!/usr/bin/env python3
"""
S-ROI Sovereign Control Protocol - Test Suite

Test completo per il protocollo S-ROI Sovereign, inclusi:
- Gestione stati
- Sistema di logging
- Cooldown stealth mode
- Thresholds e edge cases
"""

import unittest
import time
import logging
from sroi_sovereign_protocol import (
    SROISovereignProtocol,
    SROIConfig,
    SROIState,
    StateManager,
    StealthModeController,
    ResonanceMonitor,
    setup_logger
)


class TestSROIConfig(unittest.TestCase):
    """Test per configurazione S-ROI."""
    
    def test_default_config(self):
        """Test configurazione di default."""
        config = SROIConfig()
        
        self.assertEqual(config.normal_threshold, 0.7)
        self.assertEqual(config.warning_threshold, 0.85)
        self.assertEqual(config.critical_threshold, 0.95)
        self.assertEqual(config.stealth_cooldown_seconds, 60.0)
    
    def test_custom_config(self):
        """Test configurazione personalizzata."""
        config = SROIConfig(
            normal_threshold=0.6,
            warning_threshold=0.8,
            critical_threshold=0.9,
            stealth_cooldown_seconds=30.0
        )
        
        self.assertEqual(config.normal_threshold, 0.6)
        self.assertEqual(config.warning_threshold, 0.8)
        self.assertEqual(config.critical_threshold, 0.9)
        self.assertEqual(config.stealth_cooldown_seconds, 30.0)
    
    def test_valid_config(self):
        """Test validazione configurazione corretta."""
        config = SROIConfig()
        self.assertTrue(config.validate())
    
    def test_invalid_threshold_order(self):
        """Test validazione con thresholds non ordinati."""
        config = SROIConfig(
            normal_threshold=0.9,
            warning_threshold=0.7,
            critical_threshold=0.95
        )
        
        with self.assertRaises(ValueError):
            config.validate()
    
    def test_invalid_cooldown(self):
        """Test validazione con cooldown negativo."""
        config = SROIConfig(stealth_cooldown_seconds=-10.0)
        
        with self.assertRaises(ValueError):
            config.validate()
    
    def test_config_to_dict(self):
        """Test serializzazione config."""
        config = SROIConfig()
        config_dict = config.to_dict()
        
        self.assertIsInstance(config_dict, dict)
        self.assertIn('normal_threshold', config_dict)
        self.assertIn('stealth_cooldown_seconds', config_dict)


class TestStateManager(unittest.TestCase):
    """Test per gestore stati."""
    
    def setUp(self):
        """Setup per ogni test."""
        self.config = SROIConfig()
        self.logger = setup_logger(level=logging.WARNING)  # Meno verbose nei test
        self.state_manager = StateManager(self.config, self.logger)
    
    def test_initial_state(self):
        """Test stato iniziale."""
        self.assertEqual(self.state_manager.current_state, SROIState.NORMAL)
        self.assertEqual(len(self.state_manager.state_history), 0)
    
    def test_determine_state_normal(self):
        """Test determinazione stato NORMAL."""
        state = self.state_manager.determine_state(0.5)
        self.assertEqual(state, SROIState.NORMAL)
    
    def test_determine_state_warning(self):
        """Test determinazione stato WARNING."""
        state = self.state_manager.determine_state(0.87)
        self.assertEqual(state, SROIState.WARNING)
    
    def test_determine_state_critical(self):
        """Test determinazione stato CRITICAL."""
        state = self.state_manager.determine_state(0.96)
        self.assertEqual(state, SROIState.CRITICAL)
    
    def test_determine_state_at_threshold(self):
        """Test determinazione stato esattamente sulla soglia."""
        # Esattamente sulla soglia warning
        state = self.state_manager.determine_state(0.85)
        self.assertEqual(state, SROIState.WARNING)
        
        # Esattamente sulla soglia critical
        state = self.state_manager.determine_state(0.95)
        self.assertEqual(state, SROIState.CRITICAL)
    
    def test_stealth_state_preservation(self):
        """Test che STEALTH state non cambi con determine_state."""
        # Imposta manualmente a STEALTH
        self.state_manager.current_state = SROIState.STEALTH
        
        # Anche con risonanza alta, dovrebbe rimanere STEALTH
        state = self.state_manager.determine_state(0.99)
        self.assertEqual(state, SROIState.STEALTH)
    
    def test_state_transition(self):
        """Test transizione di stato."""
        self.state_manager.transition_to(
            SROIState.WARNING,
            0.87,
            "Test transition"
        )
        
        self.assertEqual(self.state_manager.current_state, SROIState.WARNING)
        self.assertEqual(len(self.state_manager.state_history), 1)
        
        event = self.state_manager.state_history[0]
        self.assertEqual(event.previous_state, SROIState.NORMAL)
        self.assertEqual(event.new_state, SROIState.WARNING)
        self.assertEqual(event.current_resonance, 0.87)
    
    def test_no_transition_same_state(self):
        """Test che non avvenga transizione se stato è uguale."""
        self.state_manager.transition_to(
            SROIState.NORMAL,
            0.5,
            "Should not transition"
        )
        
        self.assertEqual(len(self.state_manager.state_history), 0)
    
    def test_get_state_history(self):
        """Test recupero storia stati."""
        # Crea alcune transizioni
        self.state_manager.transition_to(SROIState.WARNING, 0.87, "First")
        self.state_manager.transition_to(SROIState.CRITICAL, 0.96, "Second")
        self.state_manager.transition_to(SROIState.NORMAL, 0.5, "Third")
        
        history = self.state_manager.get_state_history()
        self.assertEqual(len(history), 3)
        
        # Verifica struttura
        self.assertIn('previous_state', history[0])
        self.assertIn('new_state', history[0])
        self.assertIn('current_resonance', history[0])
    
    def test_get_state_history_limited(self):
        """Test recupero storia stati con limite."""
        # Crea 5 transizioni
        for i in range(5):
            self.state_manager.current_state = SROIState.NORMAL
            self.state_manager.transition_to(SROIState.WARNING, 0.87, f"Trans {i}")
            self.state_manager.current_state = SROIState.WARNING
        
        # Recupera solo ultime 2
        history = self.state_manager.get_state_history(limit=2)
        self.assertEqual(len(history), 2)


class TestStealthModeController(unittest.TestCase):
    """Test per controller stealth mode."""
    
    def setUp(self):
        """Setup per ogni test."""
        self.config = SROIConfig(stealth_cooldown_seconds=2.0)  # 2 secondi per test
        self.logger = setup_logger(level=logging.WARNING)
        self.controller = StealthModeController(self.config, self.logger)
    
    def test_initial_state(self):
        """Test stato iniziale."""
        can_activate, reason = self.controller.can_activate()
        self.assertTrue(can_activate)
        self.assertIsNone(reason)
        self.assertEqual(self.controller.activation_count, 0)
    
    def test_first_activation(self):
        """Test prima attivazione."""
        result = self.controller.activate()
        
        self.assertTrue(result)
        self.assertEqual(self.controller.activation_count, 1)
        self.assertIsNotNone(self.controller.last_activation_time)
    
    def test_cooldown_blocking(self):
        """Test che cooldown blocchi seconda attivazione."""
        # Prima attivazione
        self.controller.activate()
        
        # Seconda attivazione immediata dovrebbe fallire
        can_activate, reason = self.controller.can_activate()
        self.assertFalse(can_activate)
        self.assertIsNotNone(reason)
        self.assertIn("Cooldown", reason)
    
    def test_cooldown_expiration(self):
        """Test che cooldown scada dopo il tempo."""
        # Attiva
        self.controller.activate()
        
        # Attendi scadenza cooldown
        time.sleep(2.1)  # Leggermente più del cooldown
        
        # Ora dovrebbe funzionare
        can_activate, reason = self.controller.can_activate()
        self.assertTrue(can_activate)
        self.assertIsNone(reason)
    
    def test_multiple_activations(self):
        """Test attivazioni multiple dopo cooldown."""
        # Prima attivazione
        self.controller.activate()
        self.assertEqual(self.controller.activation_count, 1)
        
        # Attendi cooldown
        time.sleep(2.1)
        
        # Seconda attivazione
        result = self.controller.activate()
        self.assertTrue(result)
        self.assertEqual(self.controller.activation_count, 2)
    
    def test_get_cooldown_status_no_activation(self):
        """Test status cooldown senza attivazioni."""
        status = self.controller.get_cooldown_status()
        
        self.assertFalse(status['is_on_cooldown'])
        self.assertEqual(status['remaining_seconds'], 0)
        self.assertTrue(status['can_activate'])
    
    def test_get_cooldown_status_active(self):
        """Test status cooldown quando attivo."""
        self.controller.activate()
        
        status = self.controller.get_cooldown_status()
        
        self.assertTrue(status['is_on_cooldown'])
        self.assertGreater(status['remaining_seconds'], 0)
        self.assertFalse(status['can_activate'])
        self.assertEqual(status['activation_count'], 1)


class TestResonanceMonitor(unittest.TestCase):
    """Test per monitor risonanza."""
    
    def setUp(self):
        """Setup per ogni test."""
        self.config = SROIConfig()
        self.logger = setup_logger(level=logging.WARNING)
        self.monitor = ResonanceMonitor(self.config, self.logger)
    
    def test_initial_resonance(self):
        """Test risonanza iniziale."""
        self.assertEqual(self.monitor.current_resonance, 0.0)
        self.assertEqual(len(self.monitor.resonance_history), 0)
    
    def test_update_resonance(self):
        """Test aggiornamento risonanza."""
        self.monitor.update_resonance(0.75)
        
        self.assertEqual(self.monitor.current_resonance, 0.75)
        self.assertEqual(len(self.monitor.resonance_history), 1)
    
    def test_resonance_bounds_clamping(self):
        """Test che valori fuori range vengano clampati."""
        # Valore sopra massimo
        self.monitor.update_resonance(1.5)
        self.assertEqual(self.monitor.current_resonance, 1.0)
        
        # Valore sotto minimo
        self.monitor.update_resonance(-0.5)
        self.assertEqual(self.monitor.current_resonance, 0.0)
    
    def test_resonance_history_tracking(self):
        """Test tracciamento storia risonanza."""
        values = [0.1, 0.3, 0.5, 0.7, 0.9]
        
        for value in values:
            self.monitor.update_resonance(value)
        
        self.assertEqual(len(self.monitor.resonance_history), 5)
        
        # Verifica struttura
        for i, entry in enumerate(self.monitor.resonance_history):
            self.assertIn('timestamp', entry)
            self.assertIn('value', entry)
            self.assertEqual(entry['value'], values[i])
    
    def test_resonance_stats_empty(self):
        """Test statistiche con storia vuota."""
        stats = self.monitor.get_resonance_stats()
        
        self.assertEqual(stats['current'], 0.0)
        self.assertEqual(stats['min'], 0.0)
        self.assertEqual(stats['max'], 0.0)
        self.assertEqual(stats['sample_count'], 0)
    
    def test_resonance_stats(self):
        """Test statistiche risonanza."""
        values = [0.2, 0.4, 0.6, 0.8, 1.0]
        
        for value in values:
            self.monitor.update_resonance(value)
        
        stats = self.monitor.get_resonance_stats()
        
        self.assertEqual(stats['current'], 1.0)
        self.assertEqual(stats['min'], 0.2)
        self.assertEqual(stats['max'], 1.0)
        self.assertEqual(stats['avg'], 0.6)
        self.assertEqual(stats['sample_count'], 5)
    
    def test_history_size_limit(self):
        """Test che la storia non ecceda il limite."""
        # Imposta limite più basso per test
        self.monitor.max_history_size = 10
        
        # Aggiungi più valori del limite
        for i in range(20):
            self.monitor.update_resonance(float(i) / 100.0)
        
        # Dovrebbe mantenere solo ultimi 10
        self.assertEqual(len(self.monitor.resonance_history), 10)


class TestSROISovereignProtocol(unittest.TestCase):
    """Test per protocollo completo S-ROI Sovereign."""
    
    def setUp(self):
        """Setup per ogni test."""
        self.config = SROIConfig(stealth_cooldown_seconds=1.0)  # 1 secondo per test
        self.logger = setup_logger(level=logging.WARNING)
        self.protocol = SROISovereignProtocol(config=self.config, logger=self.logger)
    
    def test_initialization(self):
        """Test inizializzazione protocollo."""
        self.assertIsNotNone(self.protocol.state_manager)
        self.assertIsNotNone(self.protocol.stealth_controller)
        self.assertIsNotNone(self.protocol.resonance_monitor)
        self.assertEqual(self.protocol.get_current_state(), SROIState.NORMAL)
    
    def test_update_resonance_normal(self):
        """Test update risonanza in range normale."""
        self.protocol.update_resonance(0.5)
        
        self.assertEqual(self.protocol.get_current_state(), SROIState.NORMAL)
        self.assertEqual(self.protocol.resonance_monitor.current_resonance, 0.5)
    
    def test_update_resonance_warning(self):
        """Test transizione automatica a WARNING."""
        self.protocol.update_resonance(0.87)
        
        self.assertEqual(self.protocol.get_current_state(), SROIState.WARNING)
    
    def test_update_resonance_critical(self):
        """Test transizione automatica a CRITICAL."""
        self.protocol.update_resonance(0.96)
        
        self.assertEqual(self.protocol.get_current_state(), SROIState.CRITICAL)
    
    def test_state_transitions_sequence(self):
        """Test sequenza completa di transizioni."""
        # NORMAL -> WARNING
        self.protocol.update_resonance(0.87)
        self.assertEqual(self.protocol.get_current_state(), SROIState.WARNING)
        
        # WARNING -> CRITICAL
        self.protocol.update_resonance(0.97)
        self.assertEqual(self.protocol.get_current_state(), SROIState.CRITICAL)
        
        # CRITICAL -> WARNING
        self.protocol.update_resonance(0.88)
        self.assertEqual(self.protocol.get_current_state(), SROIState.WARNING)
        
        # WARNING -> NORMAL
        self.protocol.update_resonance(0.6)
        self.assertEqual(self.protocol.get_current_state(), SROIState.NORMAL)
    
    def test_activate_stealth_mode(self):
        """Test attivazione stealth mode."""
        result = self.protocol.activate_stealth_mode()
        
        self.assertTrue(result)
        self.assertEqual(self.protocol.get_current_state(), SROIState.STEALTH)
    
    def test_stealth_mode_cooldown(self):
        """Test cooldown stealth mode."""
        # Prima attivazione
        self.protocol.activate_stealth_mode()
        self.protocol.deactivate_stealth_mode()
        
        # Seconda attivazione immediata dovrebbe fallire
        result = self.protocol.activate_stealth_mode()
        self.assertFalse(result)
        self.assertNotEqual(self.protocol.get_current_state(), SROIState.STEALTH)
    
    def test_deactivate_stealth_to_normal(self):
        """Test disattivazione stealth con risonanza normale."""
        self.protocol.update_resonance(0.5)
        self.protocol.activate_stealth_mode()
        
        self.protocol.deactivate_stealth_mode()
        
        self.assertEqual(self.protocol.get_current_state(), SROIState.NORMAL)
    
    def test_deactivate_stealth_to_warning(self):
        """Test disattivazione stealth con risonanza warning."""
        self.protocol.update_resonance(0.87)
        time.sleep(1.1)  # Attendi cooldown
        self.protocol.activate_stealth_mode()
        
        self.protocol.deactivate_stealth_mode()
        
        self.assertEqual(self.protocol.get_current_state(), SROIState.WARNING)
    
    def test_deactivate_stealth_to_critical(self):
        """Test disattivazione stealth con risonanza critica."""
        self.protocol.update_resonance(0.97)
        time.sleep(1.1)
        self.protocol.activate_stealth_mode()
        
        self.protocol.deactivate_stealth_mode()
        
        self.assertEqual(self.protocol.get_current_state(), SROIState.CRITICAL)
    
    def test_stealth_prevents_auto_transitions(self):
        """Test che STEALTH previene transizioni automatiche."""
        self.protocol.activate_stealth_mode()
        
        # Aggiorna con risonanza critica
        self.protocol.update_resonance(0.99)
        
        # Dovrebbe rimanere in STEALTH
        self.assertEqual(self.protocol.get_current_state(), SROIState.STEALTH)
    
    def test_get_status(self):
        """Test recupero status completo."""
        self.protocol.update_resonance(0.75)
        
        status = self.protocol.get_status()
        
        self.assertIn('protocol_version', status)
        self.assertIn('current_state', status)
        self.assertIn('resonance', status)
        self.assertIn('stealth_cooldown', status)
        self.assertIn('config', status)
        self.assertIn('timestamp', status)
        
        self.assertEqual(status['current_state'], 'NORMAL')
    
    def test_get_state_history(self):
        """Test recupero storia stati."""
        self.protocol.update_resonance(0.87)  # -> WARNING
        self.protocol.update_resonance(0.96)  # -> CRITICAL
        
        history = self.protocol.get_state_history()
        
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['new_state'], 'WARNING')
        self.assertEqual(history[1]['new_state'], 'CRITICAL')
    
    def test_export_logs(self):
        """Test export completo dei logs."""
        self.protocol.update_resonance(0.87)
        
        logs = self.protocol.export_logs()
        
        self.assertIn('status', logs)
        self.assertIn('state_history', logs)
        self.assertIn('resonance_history', logs)
    
    def test_edge_case_boundary_values(self):
        """Test casi limite con valori ai confini."""
        # Esattamente sulla soglia normal
        self.protocol.update_resonance(0.7)
        self.assertEqual(self.protocol.get_current_state(), SROIState.NORMAL)
        
        # Esattamente sulla soglia warning
        self.protocol.update_resonance(0.85)
        self.assertEqual(self.protocol.get_current_state(), SROIState.WARNING)
        
        # Esattamente sulla soglia critical
        self.protocol.update_resonance(0.95)
        self.assertEqual(self.protocol.get_current_state(), SROIState.CRITICAL)
    
    def test_rapid_updates(self):
        """Test aggiornamenti rapidi di risonanza."""
        # Simula molti aggiornamenti rapidi
        for i in range(100):
            value = (i % 100) / 100.0
            self.protocol.update_resonance(value)
        
        # Dovrebbe gestirli tutti senza errori
        stats = self.protocol.resonance_monitor.get_resonance_stats()
        self.assertEqual(stats['sample_count'], 100)


class TestIntegration(unittest.TestCase):
    """Test di integrazione end-to-end."""
    
    def test_complete_workflow(self):
        """Test workflow completo."""
        # Crea protocollo
        config = SROIConfig(stealth_cooldown_seconds=0.5)
        protocol = SROISovereignProtocol(config=config)
        
        # Scenario 1: Aumento graduale fino a WARNING
        protocol.update_resonance(0.5)
        self.assertEqual(protocol.get_current_state(), SROIState.NORMAL)
        
        protocol.update_resonance(0.87)
        self.assertEqual(protocol.get_current_state(), SROIState.WARNING)
        
        # Scenario 2: Attivazione stealth
        time.sleep(0.6)
        result = protocol.activate_stealth_mode()
        self.assertTrue(result)
        
        # Scenario 3: Durante stealth, risonanza cambia ma stato no
        protocol.update_resonance(0.97)
        self.assertEqual(protocol.get_current_state(), SROIState.STEALTH)
        
        # Scenario 4: Disattivazione stealth -> CRITICAL
        protocol.deactivate_stealth_mode()
        self.assertEqual(protocol.get_current_state(), SROIState.CRITICAL)
        
        # Scenario 5: Ritorno a normale
        protocol.update_resonance(0.3)
        self.assertEqual(protocol.get_current_state(), SROIState.NORMAL)
        
        # Verifica storia
        history = protocol.get_state_history()
        self.assertGreaterEqual(len(history), 4)


def run_tests():
    """Esegue tutti i test."""
    # Crea test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Aggiungi tutte le test class
    suite.addTests(loader.loadTestsFromTestCase(TestSROIConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestStateManager))
    suite.addTests(loader.loadTestsFromTestCase(TestStealthModeController))
    suite.addTests(loader.loadTestsFromTestCase(TestResonanceMonitor))
    suite.addTests(loader.loadTestsFromTestCase(TestSROISovereignProtocol))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Esegui test
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Ritorna stato successo
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
