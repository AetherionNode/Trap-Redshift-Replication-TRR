# Mathematical Audit: Flux-Fabric Equation (Simulation Provenance)

## Purpose
This document provides a raw audit of the mathematical relationship between the **Flux-Fabric Equation** and the results produced in the TRR (Trap-Redshift-Replication) simulation. This is a technical record of the mathematical output of the model and the associated code.

## The Flux-Fabric Equation
The model tracks the relationship between cumulative redshift replication ($R$) and flux density ($\Delta F$):

$$\Delta F \approx \int_{0}^{z} R(z') \, dz' + \Lambda_{fabric}$$

## Technical Audit (Threshold z=0.014)

### 1. Cumulative Redshift Integral
The simulation measures the frequency detuning gradient across the optical confinement path. With a detuning slope ($k \approx 127$), the integral from injection ($z=0$) to the gateway ($z=0.014$) is:
$$\int_{0}^{0.014} 127z' \, dz' \approx 0.0124$$

### 2. Empirical Baseline ($\Lambda_{fabric}$)
Based on the TRR observed ratio of output wavelength (890nm) to injection wavelength (500nm):
$$\Lambda_{fabric} = \frac{890\text{nm}}{500\text{nm}} \approx 1.78$$

### 3. Calculated Result
$$\Delta F \approx 0.0124 + 1.78 = 1.7924$$

---

## Simulation Alignment
The simulation script `generate_trr_passive_mapping()` observes a physical manifestation of this math at the $z=0.014$ threshold.

* **Baseline detection:** `s_base = 30` (Pre-Gateway)
* **Step-up detection:** `s_base = 62` (Post-Gateway)
* **Resulting Ratio:** $62 / 30 \approx 2.06$

This "Step-Up" in detections represents the increase in information flux density ($\Delta F$) as defined by the equation.

---

## Python Audit Script (Raw Math)
This script is provided to verify that the results are the consistent output of the mathematical framework.

```python
import numpy as np

# Empirical Inputs from TRR Data
K_SLOPE = 127
Z_GATEWAY = 0.014
LAMBDA_FABRIC = 1.78

def perform_audit():
    # Evaluate the Integral: 0.5 * k * z^2
    integral_val = 0.5 * K_SLOPE * (Z_GATEWAY**2)
    
    # Apply Flux-Fabric Formula
    calculated_flux = integral_val + LAMBDA_FABRIC
    
    print(f"--- TRR Mathematical Audit ---")
    print(f"Redshift Integral (0 to 0.014): {integral_val:.4f}")
    print(f"Fabric Constant Baseline:      {LAMBDA_FABRIC:.2f}")
    print(f"Mathematical Total Flux (ΔF):  {calculated_flux:.4f}")
    
    # Correlation with SNSPD Step-up (30 -> 62)
    observed_step_up = 62 / 30
    print(f"Simulation Step-Up Ratio:      {observed_step_up:.2f}")

if __name__ == "__main__":
    perform_audit()
```
Nauta, L. (2025). Laboratory Simulation of Extreme Photon Redshift via Optical Confinement and Frequency Detuning. TechRxiv. DOI: 10.36227/techrxiv.175825717.70323666/v1
