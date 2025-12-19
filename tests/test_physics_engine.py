# tests/test_physics_engine.py
import unittest
from src.physics_engine import TRRParams, PhysicsEngine

class TestPhysicsEngine(unittest.TestCase):
    def setUp(self):
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

    def test_detuning(self):
        det = PhysicsEngine.compute_detuning(self.params)
        self.assertIn('z', det)
        self.assertGreater(det['z'], 0)

    def test_coupling_efficiency(self):
        nc = PhysicsEngine.coupling_efficiency(self.params)
        self.assertTrue(0.0 <= nc <= 1.0)

    def test_coherence_time(self):
        Tc = PhysicsEngine.coherence_time(self.params)
        self.assertGreaterEqual(Tc, 0.0)

    def test_escape_probability(self):
        det = PhysicsEngine.compute_detuning(self.params)
        nc = PhysicsEngine.coupling_efficiency(self.params)
        Tc = PhysicsEngine.coherence_time(self.params)
        esc = PhysicsEngine.escape_probability(det['z'], nc, Tc)
        self.assertTrue(0.0 <= esc <= 1.0)

if __name__ == "__main__":
    unittest.main()
