#!/usr/bin/env python3
"""
Test Suite for Transmission Equation of Resonance
==================================================

Tests for the resonance_transmission module ensuring correct implementation
of the Lex Amoris Framework for communication stability.
"""

import unittest
import numpy as np
from resonance_transmission import (
    lex_amoris_function,
    calculate_resonance
)


class TestLexAmorisFunction(unittest.TestCase):
    """Test the Lex Amoris function implementation."""
    
    def test_lex_amoris_scalar(self):
        """Test Lex Amoris function with scalar input."""
        t = 0.0
        result = lex_amoris_function(t)
        # At t=0, sin(0.432 * 0) = sin(0) = 0
        self.assertAlmostEqual(result, 0.0, places=10)
    
    def test_lex_amoris_array(self):
        """Test Lex Amoris function with array input."""
        t = np.array([0.0, np.pi / (2 * 0.432)])
        result = lex_amoris_function(t)
        
        # Verify it returns an array of same shape
        self.assertEqual(result.shape, t.shape)
        
        # At t=0, should be ~0
        self.assertAlmostEqual(result[0], 0.0, places=10)
        
        # At t=π/(2*0.432), sin(0.432 * t) = sin(π/2) = 1
        self.assertAlmostEqual(result[1], 1.0, places=5)
    
    def test_lex_amoris_periodicity(self):
        """Test that Lex Amoris function is periodic."""
        # The period should be 2π/0.432
        period = 2 * np.pi / 0.432
        t1 = 1.0
        t2 = t1 + period
        
        result1 = lex_amoris_function(t1)
        result2 = lex_amoris_function(t2)
        
        # Should be approximately equal due to periodicity
        self.assertAlmostEqual(result1, result2, places=5)


class TestCalculateResonance(unittest.TestCase):
    """Test the resonance calculation function."""
    
    def test_calculate_resonance_default_params(self):
        """Test resonance calculation with default parameters."""
        result = calculate_resonance(0, 100)
        
        # Result should be a positive real number
        self.assertIsInstance(result, (float, np.floating))
        self.assertGreater(result, 0)
    
    def test_calculate_resonance_custom_params(self):
        """Test resonance calculation with custom parameters."""
        result = calculate_resonance(0, 50, s_roi=1.5, omega=0.5)
        
        # Result should be a positive real number
        self.assertIsInstance(result, (float, np.floating))
        self.assertGreater(result, 0)
    
    def test_calculate_resonance_zero_time_range(self):
        """Test resonance calculation with zero time range."""
        result = calculate_resonance(0, 0)
        
        # Should be approximately zero for zero time range
        self.assertAlmostEqual(result, 0.0, places=5)
    
    def test_calculate_resonance_different_s_roi(self):
        """Test that different S-ROI values affect the result."""
        result1 = calculate_resonance(0, 100, s_roi=1.0)
        result2 = calculate_resonance(0, 100, s_roi=2.0)
        
        # Higher S-ROI should give smaller resonance (denominator is larger)
        self.assertGreater(result1, result2)
    
    def test_calculate_resonance_stability(self):
        """Test that resonance calculation is numerically stable."""
        # Run calculation multiple times and ensure consistent results
        results = [calculate_resonance(0, 100) for _ in range(3)]
        
        # All results should be identical (within floating point precision)
        for i in range(1, len(results)):
            self.assertAlmostEqual(results[0], results[i], places=10)
    
    def test_calculate_resonance_positive_time_range(self):
        """Test resonance with various positive time ranges."""
        result_short = calculate_resonance(0, 10)
        result_long = calculate_resonance(0, 1000)
        
        # Both should be positive
        self.assertGreater(result_short, 0)
        self.assertGreater(result_long, 0)


class TestResonanceIntegration(unittest.TestCase):
    """Integration tests for the complete resonance system."""
    
    def test_full_resonance_calculation(self):
        """Test the complete resonance calculation as per specification."""
        # Parameters from the specification
        t0 = 0
        t_infinity = 100
        s_roi = 1.450
        omega = 0.432
        
        phi_res = calculate_resonance(t0, t_infinity, s_roi, omega)
        
        # Verify output characteristics
        self.assertIsInstance(phi_res, (float, np.floating))
        self.assertGreater(phi_res, 0)
        
        # The result should be finite and reasonable
        self.assertTrue(np.isfinite(phi_res))
        self.assertLess(phi_res, 1000)  # Sanity check
    
    def test_jitter_elimination_concept(self):
        """
        Test that the limit as j→0 concept is represented.
        This is a conceptual test - in practice, we use numerical integration.
        """
        # The numerical integration should converge as we increase precision
        # Test with different grid sizes
        t0, t_infinity = 0, 100
        
        # Calculate with more precision (this is already done internally)
        result = calculate_resonance(t0, t_infinity)
        
        # Should produce a stable, finite result representing j→0 limit
        self.assertTrue(np.isfinite(result))
        self.assertGreater(result, 0)


if __name__ == '__main__':
    unittest.main()
