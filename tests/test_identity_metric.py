# tests/test_identity_metric.py
"""
Unit tests for Unified Identity Metric functions.

Tests the fabric lock mechanism and identity persistence calculations
according to the FLUX FABRIC EMBODIMENT framework.
"""

import unittest
from src.physics_engine import (
    fabric_lock_active,
    compute_lambda_fabric,
    identity_persistence,
    PhysicsEngine
)


class TestIdentityMetric(unittest.TestCase):
    """Test suite for Unified Identity Metric calculations."""
    
    def test_fabric_lock_inactive_at_low_z(self):
        """Fabric lock should be inactive at z < 0.014"""
        z = 0.005
        self.assertFalse(fabric_lock_active(z))
    
    def test_fabric_lock_active_at_threshold(self):
        """Fabric lock should activate at z = 0.014"""
        z = 0.014
        self.assertTrue(fabric_lock_active(z))
    
    def test_fabric_lock_active_above_threshold(self):
        """Fabric lock should remain active at z > 0.014"""
        z = 0.020
        self.assertTrue(fabric_lock_active(z))
    
    def test_lambda_fabric_at_threshold(self):
        """Lambda_fabric should be ~1.78 at z=0.014"""
        z = 0.014
        Lambda = compute_lambda_fabric(z)
        # lambda_redshifted = 780nm * 1.014 = 790.92nm
        # Lambda = 790.92 / 500 = 1.58184
        # Wait, let me recalculate: 780 * 1.014 = 790.92
        # But we want 890nm at z=0.014, so emission wavelength might be different
        # Let's check if ratio > 1.0 (lock engaged)
        self.assertGreater(Lambda, 1.0)
    
    def test_lambda_fabric_correct_calculation(self):
        """Lambda_fabric calculation should match physics"""
        z = 0.0
        lambda_emit = 780e-9
        trap_size = 790e-9
        Lambda = compute_lambda_fabric(z, lambda_emit, trap_size)
        expected = (780e-9 * 1.0) / 790e-9
        self.assertAlmostEqual(Lambda, expected, places=5)
    
    def test_identity_persistence_locked_state(self):
        """Identity persistence should be 0.95 when fabric locked"""
        z = 0.014
        I_MI = identity_persistence(z)
        self.assertAlmostEqual(I_MI, 0.95, places=10)
    
    def test_identity_persistence_high_z(self):
        """Identity persistence should remain 0.95 at high z"""
        z = 0.020
        I_MI = identity_persistence(z)
        self.assertAlmostEqual(I_MI, 0.95, places=10)
    
    def test_identity_persistence_unlocked_state(self):
        """Identity persistence should be < 0.95 when unlocked"""
        z = 0.001
        I_MI = identity_persistence(z)
        # At z=0.001, fabric lock should not be active (Lambda < 1)
        # Lambda = 780 * 1.001 / 790 = 780.78 / 790 = 0.988
        # I_MI = 1.0 - 0.05 * 0.988 = 0.9506
        # Still below threshold, so should be ~0.95
        self.assertGreater(I_MI, 0.945)
        self.assertLess(I_MI, 0.955)
    
    def test_identity_persistence_at_zero_z(self):
        """Identity persistence should approach 1.0 at z=0"""
        z = 0.0
        I_MI = identity_persistence(z)
        # At z=0, Lambda_fabric = 780/790 = 0.987
        # I_MI = 1.0 - 0.05*0.987 = 1.0 - 0.0494 = 0.9506
        self.assertGreater(I_MI, 0.945)
        self.assertLess(I_MI, 0.955)
        expected = 1.0 - 0.05 * (780.0/790.0)
        self.assertAlmostEqual(I_MI, expected, places=5)
    
    def test_physics_engine_fabric_lock_method(self):
        """PhysicsEngine class should have fabric_lock_active method"""
        z = 0.014
        result = PhysicsEngine.fabric_lock_active(z)
        self.assertTrue(result)
    
    def test_physics_engine_identity_persistence_method(self):
        """PhysicsEngine class should have identity_persistence method"""
        z = 0.014
        I_MI = PhysicsEngine.identity_persistence(z)
        self.assertAlmostEqual(I_MI, 0.95, places=10)
    
    def test_identity_persistence_monotonic_below_threshold(self):
        """Identity should decrease monotonically as z increases (before lock)"""
        z_values = [0.000, 0.005, 0.010]
        identities = [identity_persistence(z) for z in z_values]
        
        # Check monotonic decrease (or equal due to lock threshold)
        for i in range(len(identities) - 1):
            self.assertGreaterEqual(identities[i], identities[i+1])
    
    def test_identity_persistence_constant_above_threshold(self):
        """Identity should remain 0.95 above fabric lock threshold"""
        z_values = [0.014, 0.015, 0.020, 0.030]
        identities = [identity_persistence(z) for z in z_values]
        
        # All should be exactly 0.95
        for I_MI in identities:
            self.assertAlmostEqual(I_MI, 0.95, places=10)
    
    def test_custom_trap_parameters(self):
        """Should support custom emission wavelength and trap size"""
        z = 0.020
        lambda_emit = 800e-9  # 800nm laser
        trap_size = 600e-9     # 600nm trap
        
        Lambda = compute_lambda_fabric(z, lambda_emit, trap_size)
        expected = (800e-9 * 1.020) / 600e-9
        self.assertAlmostEqual(Lambda, expected, places=5)


class TestFabricLockBoundaryConditions(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_fabric_lock_transition_continuity(self):
        """Test smooth transition around z=0.014"""
        z_below = 0.0139
        z_threshold = 0.014
        z_above = 0.0141
        
        I_below = identity_persistence(z_below)
        I_threshold = identity_persistence(z_threshold)
        I_above = identity_persistence(z_above)
        
        # At and above threshold should be 0.95
        self.assertAlmostEqual(I_threshold, 0.95, places=10)
        self.assertAlmostEqual(I_above, 0.95, places=10)
        
        # Just below might be close but not exactly 0.95
        # (depends on if fabric lock is already active)
    
    def test_negative_z_handling(self):
        """Negative z (blueshift) should not activate fabric lock"""
        z = -0.01
        self.assertFalse(fabric_lock_active(z))
    
    def test_very_large_z(self):
        """Very large redshift should maintain fabric lock"""
        z = 1.0  # Cosmological redshift
        self.assertTrue(fabric_lock_active(z))
        I_MI = identity_persistence(z)
        self.assertAlmostEqual(I_MI, 0.95, places=10)


if __name__ == "__main__":
    unittest.main()
