# src/quantum_noise_probe.py

import cirq
import numpy as np

class QuantumNoiseProbe:
    @staticmethod
    def run_cirq_noise_probe(Tc, z, nc, shots=8192):
        dep_err = np.clip(0.02 + 0.30 * z + 0.20 * (1.0 - nc), 0.0, 0.9)
        Tc_ref = 1e-3
        phase_gamma = np.clip(0.02 + 0.50 * (Tc_ref / max(Tc, 1e-12)) + 0.10 * (1.0 - nc), 0.0, 0.9)

        q0, q1 = cirq.LineQubit(0), cirq.LineQubit(1)
        circuit = cirq.Circuit()
        circuit.append(cirq.H(q0))
        circuit.append(cirq.phase_damp(gamma=phase_gamma).on(q0))
        circuit.append(cirq.depolarize(p=dep_err).on(q0))
        circuit.append(cirq.CNOT(q0, q1))
        circuit.append(cirq.depolarize(p=dep_err).on(q0))
        circuit.append(cirq.depolarize(p=dep_err).on(q1))
        circuit.append(cirq.measure(q0, q1, key='m'))

        simulator = cirq.Simulator()
        results = simulator.run(circuit, repetitions=shots)
        counts = results.histogram(key='m')

        formatted_counts = {}
        for outcome, count in counts.items():
            bit_string = format(outcome, '02b')
            formatted_counts[bit_string] = count

        p00 = formatted_counts.get('00', 0) / shots
        p11 = formatted_counts.get('11', 0) / shots
        fidelity_proxy = p00 + p11

        return {
            "counts": formatted_counts,
            "fidelity_proxy": fidelity_proxy,
            "dep_err": dep_err,
            "phase_err": phase_gamma
        }
