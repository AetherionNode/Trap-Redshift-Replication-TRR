# src/demo.py

import datetime
import numpy as np
from physics_engine import TRRParams, PhysicsEngine
from quantum_noise_probe import QuantumNoiseProbe
from logging_utils import log_to_csv


def demo():
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

    det = PhysicsEngine.compute_detuning(params)
    nc = PhysicsEngine.coupling_efficiency(params)
    Tc = PhysicsEngine.coherence_time(params)
    esc = PhysicsEngine.escape_probability(det["z"], nc, Tc)

    print("=== TRR Detuning/Redshift ===")
    print(f"Δν: {det['delta_nu']:.3e} Hz | ν_obs: {det['nu_obs']:.3e} Hz | z: {det['z']:.6f}")
    print("=== Trap Coupling & Coherence ===")
    print(f"nc: {nc:.4f} | Tc: {Tc:.3e} s | Escape Prob.: {esc:.3f}")

    qp = QuantumNoiseProbe.run_cirq_noise_probe(Tc, det["z"], nc, shots=4096)
    print("=== Cirq Noise Experiment ===")
    print(f"Depolarizing error: {qp['dep_err']:.3f} | Phase damping error: {qp['phase_err']:.3f}")
    print(f"Counts: {qp['counts']} | Fidelity proxy: {qp['fidelity_proxy']:.3f}")

    # CSV logging
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
    log_to_csv("results/trr_log.csv", log_data)
    print(f"[LOG] Run data appended to results/trr_log.csv")

    # Prepare data for plotting
    zs = np.linspace(0, min(0.9, det['z']*1.2), 12)
    fps = []
    for zval in zs:
        qp_sweep = QuantumNoiseProbe.run_cirq_noise_probe(Tc, zval, nc, shots=2048)
        fps.append(qp_sweep['fidelity_proxy'])

    return {"current_qp": qp, "sweep_data": {"zs": zs, "fps": fps}}

if __name__ == "__main__":
    results = demo()
    current_qp = results["current_qp"]
    sweep_data = results["sweep_data"]
