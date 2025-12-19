# TRR: Simulating 200M Lightyears in an Optical Trap

## Overview
Trap-Redshift-Replication (TRR) simulates a laboratory method for replicating extreme cosmological redshift ($z$) using nanoparticle-based optical traps and cascaded GHz-THz frequency detuning. This project models the quantum decoherence and fidelity loss as photons are redshifted, revealing a critical physical limit.

---

## The Benchmark
- **Frequency Shift:** 5 THz
- **Success Point:** $z = 0.013021$ (high-fidelity regime)

## The Discovery: The 0.014 Wall
At $z = 0.014$, the simulation uncovers a sharp drop in quantum coherence. Here, photon wavepackets outgrow the optical trap, causing a dramatic fidelity loss due to phase damping. This "Physical Wall" marks the **Cosmic Confinement Limit** for laboratory redshift replication.

## Technical Stack
- **Cirq:** Quantum circuit simulation and phase damping modeling
- **NumPy:** Physics calculations and parameter sweeps
- **Matplotlib:** Visualization of coherence and fidelity

## Directory Structure
```
/src      # Simulation engine and modules
/docs     # White paper and documentation
/results  # CSV logs and output graphs
/tests    # Unit tests
```

## Getting Started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the demo simulation:
   ```bash
   python src/demo.py
   ```
3. Visualize the fidelity graph:
   ```bash
   python src/visualizer.py
   ```

## Citation
White paper: See `/docs/TechRxiv TRR.pdf` (placeholder).

---

*This project demonstrates the quantum limits of simulating cosmological redshift in the lab, highlighting the interplay between detuning, trap physics, and quantum noise.*
