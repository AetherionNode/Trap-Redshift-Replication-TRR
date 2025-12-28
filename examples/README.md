# Examples

This directory contains demonstration scripts for the TRR framework.

## Identity Metric Demonstration

**File:** `demo_identity_metric.py`

Demonstrates the Unified Identity Metric and Fabric Lock mechanism across different redshift values.

### Usage

```bash
python examples/demo_identity_metric.py
```

### What It Shows

1. **Fabric Lock Threshold**: How identity persistence transitions from probabilistic to geometric constant at z=0.014
2. **Geometric Constant**: Identity remains at exactly 0.95 once fabric lock engages
3. **Information Paradox**: The 5% loss corresponds to Hawking radiation
4. **Room-Temperature Resilience**: Basis for the FLUX FABRIC EMBODIMENT patent framework

### Sample Output

```
       z |  λ_red(nm) |   Λ_fabric |   Lock |     I_MI |               Status
------------------------------------------------------------------------------------------
  0.0000 |     780.00 |     0.9873 |      ✗ | 0.950633 |        Probabilistic
  0.0140 |     790.92 |     1.0012 |      ✓ | 0.950000 |  🔒 Fabric Lock START
  0.0200 |     795.60 |     1.0071 |      ✓ | 0.950000 |      🔒 Fabric Locked
```

Key observation: At z≥0.014, I_MI locks to exactly 0.95, demonstrating geometric stabilization.
