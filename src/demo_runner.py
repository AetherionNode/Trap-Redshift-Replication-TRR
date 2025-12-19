"""
TRR Demo Runner: 5 THz Detuning Sweep Demonstration

Executes a comprehensive sweep demonstrating the approach to the z=0.014
cosmic confinement limit, logging results for analysis and visualization.
"""

import datetime
import numpy as np
from physics_engine import TRRParams, compute_detuning, coupling_efficiency, coherence_time, escape_probability
from quantum_noise_probe import run_cirq_noise_probe
from logging_utils import log_to_csv


def demo():
    """
    Main demonstration of TRR physics simulation.
    
    Initializes default parameters for 5 THz cascaded detuning (n_cycles=1000,
    f_m=5 GHz), performs single-point calculation, then executes a 12-point
    sweep from z=0 to z~0.013 to demonstrate approach to the 0.014 barrier.
    
    Returns:
        Dictionary with current quantum probe results and sweep data
    """
    # Initialize TRR parameters for 5 THz detuning
    # ν_emit = 3.84×10^14 Hz (780 nm), f_m = 5 GHz, 1000 cycles
    params = TRRParams(
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

    # Compute physics for default parameters
    det = compute_detuning(params)
    nc = coupling_efficiency(params)
    Tc = coherence_time(params)
    esc = escape_probability(det["z"], nc, Tc)

    print("=" * 60)
    print("TRR: Trap-Redshift-Replication Demonstration")
    print("=" * 60)
    print("\n=== TRR Detuning/Redshift ===")
    print(f"Δν: {det['delta_nu']:.3e} Hz | ν_obs: {det['nu_obs']:.3e} Hz | z: {det['z']:.6f}")
    print("\n=== Trap Coupling & Coherence ===")
    print(f"nc: {nc:.4f} | Tc: {Tc:.3e} s | Escape Prob.: {esc:.3f}")

    # Run quantum noise probe for current parameters
    qp = run_cirq_noise_probe(Tc, det["z"], nc, shots=4096)
    print("\n=== Cirq Noise Experiment ===")
    print(f"Depolarizing error: {qp['dep_err']:.3f} | Phase damping error: {qp['phase_err']:.3f}")
    print(f"Counts: {qp['counts']} | Fidelity proxy: {qp['fidelity_proxy']:.3f}")

    # Log single-point result
    timestamp = datetime.datetime.now().isoformat()
    log_data = {
        "timestamp": timestamp,
        "z": det["z"],
        "Tc": Tc,
        "nc": nc,
        "escape_prob": esc,
        "fidelity_proxy": qp["fidelity_proxy"],
        "dep_err": qp["dep_err"],
        "phase_err": qp["phase_err"]
    }
    log_to_csv("results/trr_simulation_log.csv", log_data)
    print(f"\n[LOG] Run data appended to results/trr_simulation_log.csv")

    # Execute 5 THz detuning sweep (12 points, z=0 to z~0.013)
    print("\n" + "=" * 60)
    print("Executing 5 THz Detuning Sweep (12 points)")
    print("=" * 60)
    
    zs = np.linspace(0, min(0.9, det['z'] * 1.2), 12)
    fps = []
    
    print(f"\n{'z':>8s} | {'Fidelity':>10s} | {'Phase Err':>10s} | {'Dep Err':>10s}")
    print("-" * 50)
    
    for i, zval in enumerate(zs):
        qp_sweep = run_cirq_noise_probe(Tc, zval, nc, shots=2048)
        fps.append(qp_sweep['fidelity_proxy'])
        
        # Print sweep progress
        print(f"{zval:8.6f} | {qp_sweep['fidelity_proxy']:10.4f} | "
              f"{qp_sweep['phase_err']:10.4f} | {qp_sweep['dep_err']:10.4f}")
        
        # Log sweep data
        sweep_log_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "z": zval,
            "Tc": Tc,
            "nc": nc,
            "escape_prob": escape_probability(zval, nc, Tc),
            "fidelity_proxy": qp_sweep['fidelity_proxy'],
            "dep_err": qp_sweep['dep_err'],
            "phase_err": qp_sweep['phase_err']
        }
        log_to_csv("results/trr_simulation_log.csv", sweep_log_data)
    
    print("\n" + "=" * 60)
    print("SUMMARY: Approaching the z = 0.014 Cosmic Confinement Limit")
    print("=" * 60)
    print(f"Maximum z simulated: {max(zs):.6f}")
    print(f"Distance to 0.014 wall: {0.014 - max(zs):.6f}")
    print(f"Final fidelity: {fps[-1]:.4f}")
    print(f"Fidelity degradation: {(1.0 - fps[-1]) * 100:.1f}%")
    print("\nNote: At z = 0.014, photon wavepackets (~890 nm) exceed")
    print("nanoparticle trap dimensions (100-500 nm), causing catastrophic")
    print("phase damping and fidelity collapse.")
    print("=" * 60)

    return {"current_qp": qp, "sweep_data": {"zs": zs, "fps": fps}}


if __name__ == "__main__":
    results = demo()
    current_qp = results["current_qp"]
    sweep_data = results["sweep_data"]
