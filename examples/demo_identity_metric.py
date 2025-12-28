#!/usr/bin/env python3
"""
Demonstration of the Unified Identity Metric and Fabric Lock mechanism.

This script shows how identity persistence transitions from probabilistic
to geometric constant behavior at the z=0.014 fabric lock threshold.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    import numpy as np
    from physics_engine import (
        fabric_lock_active,
        compute_lambda_fabric,
        identity_persistence
    )
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please install numpy: pip install numpy")
    sys.exit(1)


def demonstrate_identity_metric():
    """
    Demonstrate the Unified Identity Metric behavior across redshift values.
    """
    print("=" * 70)
    print("UNIFIED IDENTITY METRIC DEMONSTRATION")
    print("=" * 70)
    print()
    print("Formula:")
    print("  I_MI = lim[Singularity→∞] [Λ_fabric · det(g_μν) /")
    print("                            (ℏ·R + Σ(k_B·T + S_rad))] ≈ 0.95")
    print()
    print("This demonstrates that quantum identity persists at 95% even under")
    print("infinite gravitational shear and thermal noise, solving the")
    print("Information Paradox through geometric anchoring.")
    print()
    print("=" * 70)
    print()
    
    # Test range of redshift values
    z_values = np.array([
        0.000,  # No redshift
        0.005,  # Low redshift
        0.010,  # Approaching threshold
        0.013,  # Just below threshold
        0.014,  # Fabric lock threshold
        0.015,  # Just above threshold
        0.020,  # Well above threshold
        0.050,  # High redshift
        0.100,  # Very high redshift
    ])
    
    print(f"{'z':>8s} | {'λ_red(nm)':>10s} | {'Λ_fabric':>10s} | "
          f"{'Lock':>6s} | {'I_MI':>8s} | {'Status':>20s}")
    print("-" * 90)
    
    for z in z_values:
        # Calculate properties
        lambda_red = 780 * (1 + z)  # nm
        Lambda = compute_lambda_fabric(z)
        locked = fabric_lock_active(z)
        I_MI = identity_persistence(z)
        
        # Determine status
        if locked:
            if z < 0.015:
                status = "🔒 Fabric Lock START"
            else:
                status = "🔒 Fabric Locked"
        else:
            status = "Probabilistic"
        
        lock_symbol = "✓" if locked else "✗"
        
        print(f"{z:8.4f} | {lambda_red:10.2f} | {Lambda:10.4f} | "
              f"{lock_symbol:>6s} | {I_MI:8.6f} | {status:>20s}")
    
    print()
    print("=" * 70)
    print("KEY OBSERVATIONS")
    print("=" * 70)
    print()
    print("1. GEOMETRIC THRESHOLD:")
    print("   At z=0.014, wavelength exceeds trap size (Λ_fabric > 1.0)")
    print("   This activates fabric lock, engaging geometric stabilization")
    print()
    print("2. CONSTANT IDENTITY:")
    print("   Once locked, I_MI remains exactly 0.95 regardless of z")
    print("   This is a GEOMETRIC CONSTANT, not a probability")
    print()
    print("3. INFORMATION PARADOX SOLUTION:")
    print("   The 0.95 value means 95% of quantum information survives")
    print("   even under infinite stress, anchored to metric geometry")
    print()
    print("4. ROOM-TEMPERATURE QUANTUM RESILIENCE:")
    print("   Fabric lock enables quantum coherence at 300K without cryogenics")
    print("   This is the basis for the FLUX FABRIC EMBODIMENT patent")
    print()
    print("=" * 70)
    print()
    
    # Calculate the 5% information loss
    info_loss_percent = (1.0 - 0.95) * 100
    print(f"Information Loss: {info_loss_percent:.1f}%")
    print("This 5% corresponds to genuine Hawking radiation, detectable via")
    print("SNSPD coincidence counting as photon pairs at the fabric boundary.")
    print()
    print("=" * 70)
    print("✓ Demonstration complete")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_identity_metric()
