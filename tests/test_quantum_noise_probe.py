# tests/test_quantum_noise_probe.py
import unittest
from src.quantum_noise_probe import QuantumNoiseProbe

class TestQuantumNoiseProbe(unittest.TestCase):
    def test_run_cirq_noise_probe(self):
        result = QuantumNoiseProbe.run_cirq_noise_probe(Tc=1e-3, z=0.01, nc=0.5, shots=128)
        self.assertIn('fidelity_proxy', result)
        self.assertIn('counts', result)
        self.assertTrue(0.0 <= result['fidelity_proxy'] <= 1.0)

if __name__ == "__main__":
    unittest.main()
