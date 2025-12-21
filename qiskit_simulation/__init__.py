"""
Qiskit-based TRR simulation package.

This package provides Qiskit implementations for modeling the z=0.014 Wall
phenomenon and Hawking radiation analogue detection via SNSPD coincidence counting.
"""

__version__ = "1.0.0"

from .trr_qiskit_simulation import (
    TRRParams,
    coupling_efficiency,
    simulate_hawking_pairs,
    run_qiskit_noise_probe,
    main
)

__all__ = [
    "TRRParams",
    "coupling_efficiency", 
    "simulate_hawking_pairs",
    "run_qiskit_noise_probe",
    "main"
]
