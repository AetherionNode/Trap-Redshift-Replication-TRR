# tests/test_qiskit_simulation.py
"""
Unit tests for Qiskit-based TRR simulation module.
"""
import unittest
import sys
import os
import numpy as np

# Add qiskit_simulation to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'qiskit_simulation'))

from trr_qiskit_simulation import (
    TRRParams, 
    coupling_efficiency, 
    simulate_hawking_pairs,
    run_qiskit_noise_probe
)


class TestQiskitSimulation(unittest.TestCase):
    """Test cases for Qiskit TRR simulation functions."""
    
    def setUp(self):
        """Initialize test parameters."""
        self.params = TRRParams(
            nu_emit=3.84e14,
            fm=5e9,
            n_cycles=1000,
            P_in=0.01,
            P_trap=0.006,
            alpha_loss=2.0,
            L_eff=0.05,
            sigma_laser=1e6,
            sigma_mod=2e9,
            sigma_trap=5e8,
            coherence_baseline=1e-3
        )
    
    def test_coupling_efficiency(self):
        """Test coupling efficiency calculation."""
        nc = coupling_efficiency(self.params)
        self.assertTrue(0.0 <= nc <= 1.0, "Coupling efficiency out of range")
        self.assertGreater(nc, 0.0, "Coupling efficiency should be positive")
    
    def test_simulate_hawking_pairs(self):
        """Test Hawking pair simulation."""
        z = 0.014
        nc = coupling_efficiency(self.params)
        pair_prob, coincidences = simulate_hawking_pairs(z, nc)
        
        self.assertTrue(0.0 <= pair_prob <= 1.0, "Pair probability out of range")
        self.assertIsInstance(coincidences, (int, np.integer if hasattr(np, 'integer') else np.signedinteger), 
                            "Coincidences should be integer")
        self.assertGreaterEqual(coincidences, 0, "Coincidences should be non-negative")
    
    def test_hawking_pairs_increase_with_z(self):
        """Test that Hawking pair probability increases approaching z=0.014."""
        nc = coupling_efficiency(self.params)
        
        # Test at multiple redshift values
        z_values = [0.005, 0.010, 0.014]
        probs = []
        
        for z in z_values:
            pair_prob, _ = simulate_hawking_pairs(z, nc)
            probs.append(pair_prob)
        
        # Should generally increase as we approach z=0.014
        # (though with some randomness in coincidences)
        self.assertLessEqual(probs[0], probs[-1] + 0.1, 
                            "Pair probability should increase with z")
    
    def test_run_qiskit_noise_probe(self):
        """Test Qiskit noise probe execution."""
        z = 0.010
        nc = coupling_efficiency(self.params)
        
        # Run with reduced shots for faster testing
        fidelity = run_qiskit_noise_probe(z, nc, shots=256)
        
        self.assertTrue(0.0 <= fidelity <= 1.0, "Fidelity out of range")
        self.assertIsInstance(fidelity, (float, np.floating if hasattr(np, 'floating') else np.float64), 
                            "Fidelity should be float")
    
    def test_fidelity_decreases_with_z(self):
        """Test that fidelity generally decreases with increasing redshift."""
        nc = coupling_efficiency(self.params)
        
        # Test at two redshift values
        z_low = 0.000
        z_high = 0.020
        
        fidelity_low = run_qiskit_noise_probe(z_low, nc, shots=512)
        fidelity_high = run_qiskit_noise_probe(z_high, nc, shots=512)
        
        # Allow some tolerance due to quantum randomness
        # Generally, higher z should have lower or similar fidelity
        self.assertLessEqual(fidelity_high, fidelity_low + 0.2,
                            "Fidelity should decrease or stay similar with higher z")
    
    def test_z_014_wall_behavior(self):
        """Test behavior at the critical z=0.014 wall."""
        nc = coupling_efficiency(self.params)
        z_wall = 0.014
        
        # Test fidelity
        fidelity = run_qiskit_noise_probe(z_wall, nc, shots=512)
        self.assertTrue(0.0 <= fidelity <= 1.0)
        
        # Test Hawking pairs
        pair_prob, coincidences = simulate_hawking_pairs(z_wall, nc)
        self.assertTrue(0.0 <= pair_prob <= 1.0)
        self.assertGreaterEqual(coincidences, 0)


if __name__ == "__main__":
    unittest.main()
