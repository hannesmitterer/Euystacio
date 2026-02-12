#!/usr/bin/env python3
"""
Transmission Equation of Resonance - Test Suite

Comprehensive tests for the resonance transmission implementation,
ensuring accurate calculation of the Lex Amoris Framework equations.
"""

import unittest
import numpy as np
from resonance_transmission import (
    lex_amoris_function,
    calculate_resonance,
    get_resonance_magnitude,
    get_resonance_phase,
    calculate_jitter_elimination_factor,
    analyze_resonance_packet,
    OMEGA_HZ,
    S_ROI
)


class TestLexAmorisFunction(unittest.TestCase):
    """Test the Lex Amoris function."""
    
    def test_single_value(self):
        """Test Lex Amoris function with single value."""
        result = lex_amoris_function(0.0)
        self.assertAlmostEqual(result, 0.0, places=10)
        
    def test_array_values(self):
        """Test Lex Amoris function with array."""
        t = np.array([0.0, np.pi/(2*OMEGA_HZ)])
        result = lex_amoris_function(t)
        
        self.assertEqual(len(result), 2)
        self.assertAlmostEqual(result[0], 0.0, places=10)
        self.assertAlmostEqual(result[1], 1.0, places=5)
    
    def test_periodicity(self):
        """Test that function has expected periodicity."""
        period = 2 * np.pi / OMEGA_HZ
        t = 0.0
        
        value1 = lex_amoris_function(t)
        value2 = lex_amoris_function(t + period)
        
        self.assertAlmostEqual(value1, value2, places=5)


class TestCalculateResonance(unittest.TestCase):
    """Test resonance calculation."""
    
    def test_zero_interval(self):
        """Test with zero-length time interval."""
        result = calculate_resonance(0.0, 0.0)
        self.assertAlmostEqual(abs(result), 0.0, places=5)
    
    def test_positive_interval(self):
        """Test with positive time interval."""
        result = calculate_resonance(0.0, 10.0)
        
        # Result should be a complex number
        self.assertIsInstance(result, complex)
        
        # Magnitude should be positive
        magnitude = abs(result)
        self.assertGreater(magnitude, 0.0)
    
    def test_default_parameters(self):
        """Test that default parameters match constants."""
        result1 = calculate_resonance(0.0, 5.0)
        result2 = calculate_resonance(0.0, 5.0, s_roi=S_ROI, omega=OMEGA_HZ)
        
        self.assertAlmostEqual(abs(result1), abs(result2), places=5)
    
    def test_custom_parameters(self):
        """Test with custom parameters."""
        result = calculate_resonance(0.0, 10.0, s_roi=2.0, omega=0.5)
        
        # Should still return valid complex number
        self.assertIsInstance(result, complex)
        self.assertGreater(abs(result), 0.0)
    
    def test_custom_lex_amoris(self):
        """Test with custom Lex Amoris function."""
        def custom_func(t):
            return np.cos(0.5 * t)
        
        result = calculate_resonance(
            0.0, 10.0,
            lex_amoris_func=custom_func
        )
        
        self.assertIsInstance(result, complex)
    
    def test_num_points_parameter(self):
        """Test varying number of integration points."""
        result1 = calculate_resonance(0.0, 10.0, num_points=500)
        result2 = calculate_resonance(0.0, 10.0, num_points=2000)
        
        # Results should be similar but not identical
        self.assertAlmostEqual(abs(result1), abs(result2), places=2)


class TestResonanceComponents(unittest.TestCase):
    """Test extraction of resonance components."""
    
    def test_get_magnitude(self):
        """Test magnitude extraction."""
        phi_res = 3.0 + 4.0j
        magnitude = get_resonance_magnitude(phi_res)
        
        self.assertAlmostEqual(magnitude, 5.0, places=10)
    
    def test_get_phase(self):
        """Test phase extraction."""
        phi_res = 1.0 + 1.0j
        phase = get_resonance_phase(phi_res)
        
        # Should be π/4 radians (45 degrees)
        self.assertAlmostEqual(phase, np.pi/4, places=10)
    
    def test_magnitude_positive(self):
        """Test that magnitude is always positive."""
        test_values = [
            1.0 + 2.0j,
            -1.0 + 2.0j,
            -1.0 - 2.0j,
            1.0 - 2.0j
        ]
        
        for val in test_values:
            magnitude = get_resonance_magnitude(val)
            self.assertGreater(magnitude, 0.0)
    
    def test_phase_range(self):
        """Test that phase is in expected range."""
        phi_res = calculate_resonance(0.0, 10.0)
        phase = get_resonance_phase(phi_res)
        
        # Phase should be in [-π, π]
        self.assertGreaterEqual(phase, -np.pi)
        self.assertLessEqual(phase, np.pi)


class TestJitterElimination(unittest.TestCase):
    """Test jitter elimination calculations."""
    
    def test_baseline_jitter(self):
        """Test with default baseline jitter."""
        phi_res = calculate_resonance(0.0, 10.0)
        factor = calculate_jitter_elimination_factor(phi_res)
        
        # Factor should be between 0 and 1
        self.assertGreaterEqual(factor, 0.0)
        self.assertLessEqual(factor, 1.0)
    
    def test_custom_baseline(self):
        """Test with custom baseline jitter."""
        phi_res = calculate_resonance(0.0, 10.0)
        factor = calculate_jitter_elimination_factor(phi_res, baseline_jitter=2.0)
        
        # Factor should still be positive
        self.assertGreater(factor, 0.0)
    
    def test_higher_magnitude_better_elimination(self):
        """Test that higher magnitude leads to better jitter elimination."""
        # Create two scenarios with different magnitudes
        phi_low = 1.0 + 0.5j   # Lower magnitude
        phi_high = 5.0 + 3.0j  # Higher magnitude
        
        factor_low = calculate_jitter_elimination_factor(phi_low)
        factor_high = calculate_jitter_elimination_factor(phi_high)
        
        # Higher magnitude should result in lower factor (better elimination)
        self.assertLess(factor_high, factor_low)
    
    def test_zero_magnitude(self):
        """Test behavior with zero magnitude."""
        phi_res = 0.0 + 0.0j
        factor = calculate_jitter_elimination_factor(phi_res, baseline_jitter=1.0)
        
        # Should return baseline jitter
        self.assertEqual(factor, 1.0)


class TestAnalyzeResonancePacket(unittest.TestCase):
    """Test comprehensive resonance analysis."""
    
    def test_analysis_structure(self):
        """Test that analysis returns expected structure."""
        analysis = analyze_resonance_packet(0.0, 10.0)
        
        # Check all expected keys
        self.assertIn('phi_res', analysis)
        self.assertIn('magnitude', analysis)
        self.assertIn('phase', analysis)
        self.assertIn('phase_degrees', analysis)
        self.assertIn('jitter_elimination', analysis)
        self.assertIn('parameters', analysis)
    
    def test_analysis_parameters(self):
        """Test that parameters are correctly stored."""
        t0, t_inf = 0.0, 15.0
        s_roi, omega = 1.5, 0.5
        
        analysis = analyze_resonance_packet(t0, t_inf, s_roi, omega)
        
        params = analysis['parameters']
        self.assertEqual(params['t0'], t0)
        self.assertEqual(params['t_infinity'], t_inf)
        self.assertEqual(params['s_roi'], s_roi)
        self.assertEqual(params['omega'], omega)
    
    def test_phase_degrees_conversion(self):
        """Test that phase is correctly converted to degrees."""
        analysis = analyze_resonance_packet(0.0, 10.0)
        
        phase_rad = analysis['phase']
        phase_deg = analysis['phase_degrees']
        
        # Verify conversion
        self.assertAlmostEqual(
            phase_deg,
            np.degrees(phase_rad),
            places=5
        )
    
    def test_analysis_values_valid(self):
        """Test that all analysis values are valid numbers."""
        analysis = analyze_resonance_packet(0.0, 10.0)
        
        # Check that values are not NaN or Inf
        self.assertTrue(np.isfinite(analysis['magnitude']))
        self.assertTrue(np.isfinite(analysis['phase']))
        self.assertTrue(np.isfinite(analysis['phase_degrees']))
        self.assertTrue(np.isfinite(analysis['jitter_elimination']))


class TestConstants(unittest.TestCase):
    """Test module constants."""
    
    def test_omega_value(self):
        """Test that OMEGA_HZ has expected value."""
        self.assertEqual(OMEGA_HZ, 0.432)
    
    def test_s_roi_value(self):
        """Test that S_ROI has expected value."""
        self.assertEqual(S_ROI, 1.450)


class TestParameterSensitivity(unittest.TestCase):
    """Test sensitivity to parameter variations."""
    
    def test_s_roi_sensitivity(self):
        """Test how S-ROI affects results."""
        base_result = calculate_resonance(0.0, 10.0, s_roi=1.450)
        high_result = calculate_resonance(0.0, 10.0, s_roi=2.0)
        low_result = calculate_resonance(0.0, 10.0, s_roi=1.0)
        
        # Different S-ROI should give different magnitudes
        base_mag = abs(base_result)
        high_mag = abs(high_result)
        low_mag = abs(low_result)
        
        # Higher S-ROI should decrease magnitude (dividing by larger number)
        self.assertGreater(base_mag, high_mag)
        self.assertLess(base_mag, low_mag)
    
    def test_omega_sensitivity(self):
        """Test how omega affects results."""
        base_result = calculate_resonance(0.0, 10.0, omega=0.432)
        diff_result = calculate_resonance(0.0, 10.0, omega=0.5)
        
        # Different omega should give different results
        self.assertNotAlmostEqual(abs(base_result), abs(diff_result), places=3)
    
    def test_time_interval_sensitivity(self):
        """Test how time interval affects results."""
        short_result = calculate_resonance(0.0, 5.0)
        long_result = calculate_resonance(0.0, 20.0)
        
        # Longer integration time typically gives larger magnitude
        self.assertNotAlmostEqual(abs(short_result), abs(long_result), places=2)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLexAmorisFunction))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculateResonance))
    suite.addTests(loader.loadTestsFromTestCase(TestResonanceComponents))
    suite.addTests(loader.loadTestsFromTestCase(TestJitterElimination))
    suite.addTests(loader.loadTestsFromTestCase(TestAnalyzeResonancePacket))
    suite.addTests(loader.loadTestsFromTestCase(TestConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestParameterSensitivity))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
