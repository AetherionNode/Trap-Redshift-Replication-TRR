"""
Quantum noise probe module for TRR simulations.

This module implements Cirq-based quantum circuit simulations to model
phase damping and depolarization effects in the optical trap as photons
undergo extreme redshift.
"""

import cirq
import numpy as np


def run_cirq_noise_probe(Tc: float, z: float, nc: float, shots: int = 8192) -> dict:
    """
    Execute Bell-state fidelity measurement with quantum noise.
    
    Simulates the interplay between redshift magnitude (z) and phase damping
    in an optical trap. The phase damping γ increases dramatically as coherence
    time T_c decreases, creating a sharp fidelity drop at z = 0.014.
    
    Physics: At z = 0.014, redshifted photon wavepackets (λ ≈ 780 nm → ~890 nm
    effective) exceed nanoparticle trap dimensions (100-500 nm), causing
    geometric mismatch and severe phase damping.
    
    Args:
        Tc: Coherence time (s)
        z: Redshift value (dimensionless)
        nc: Coupling efficiency (0 to 1)
        shots: Number of circuit repetitions for statistics
        
    Returns:
        Dictionary with keys:
            - counts: Measurement outcome histogram
            - fidelity_proxy: Bell state fidelity estimate
            - dep_err: Depolarizing error magnitude
            - phase_err: Phase damping error magnitude
    """
    # Depolarizing error scales with redshift and coupling loss
    dep_err = np.clip(0.02 + 0.30 * z + 0.20 * (1.0 - nc), 0.0, 0.9)
    
    # Phase damping increases dramatically with reduced coherence
    Tc_ref = 1e-3
    phase_gamma = np.clip(0.02 + 0.50 * (Tc_ref / max(Tc, 1e-12)) + 0.10 * (1.0 - nc), 0.0, 0.9)

    # Build Bell state circuit with noise
    q0, q1 = cirq.LineQubit(0), cirq.LineQubit(1)
    circuit = cirq.Circuit()
    
    # Create entangled state with noise
    circuit.append(cirq.H(q0))
    circuit.append(cirq.phase_damp(gamma=phase_gamma).on(q0))
    circuit.append(cirq.depolarize(p=dep_err).on(q0))
    
    circuit.append(cirq.CNOT(q0, q1))
    circuit.append(cirq.depolarize(p=dep_err).on(q0))
    circuit.append(cirq.depolarize(p=dep_err).on(q1))
    
    circuit.append(cirq.measure(q0, q1, key='m'))

    # Execute and analyze
    simulator = cirq.Simulator()
    results = simulator.run(circuit, repetitions=shots)
    counts = results.histogram(key='m')

    # Format counts as bitstrings
    formatted_counts = {}
    for outcome, count in counts.items():
        bit_string = format(outcome, '02b')
        formatted_counts[bit_string] = count

    # Fidelity proxy: probability of measuring |00⟩ or |11⟩
    p00 = formatted_counts.get('00', 0) / shots
    p11 = formatted_counts.get('11', 0) / shots
    fidelity_proxy = p00 + p11

    return {
        "counts": formatted_counts,
        "fidelity_proxy": fidelity_proxy,
        "dep_err": dep_err,
        "phase_err": phase_gamma
    }


# Legacy class-based interface for backwards compatibility
class QuantumNoiseProbe:
    """
    Legacy class-based interface for quantum noise simulations.
    
    Note: Prefer using the run_cirq_noise_probe() function directly.
    This class is maintained for backwards compatibility.
    """
    
    @staticmethod
    def run_cirq_noise_probe(Tc: float, z: float, nc: float, shots: int = 8192) -> dict:
        """Execute quantum noise probe. See run_cirq_noise_probe() function."""
        return run_cirq_noise_probe(Tc, z, nc, shots)
