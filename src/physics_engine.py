"""
Physics engine for TRR (Trap-Redshift-Replication) simulations.

This module contains the core physics calculations for modeling
cascaded frequency detuning in optical traps and the resulting
redshift effects.
"""

import numpy as np


class TRRParams:
    """
    Container for TRR experimental parameters.
    
    Attributes:
        nu_emit (float): Emission frequency (Hz)
        fm (float): Modulation frequency (Hz)
        n_cycles (int): Number of modulation cycles
        P_in (float): Input power (W)
        P_trap (float): Trap power (W)
        alpha_loss (float): Loss coefficient (m^-1)
        L_eff (float): Effective trap length (m)
        sigma_laser (float): Laser noise (Hz)
        sigma_mod (float): Modulation noise (Hz)
        sigma_trap (float): Trap noise (Hz)
        coherence_baseline (float): Baseline coherence time (s)
    """
    
    def __init__(self, nu_emit: float, fm: float, n_cycles: int,
                 P_in: float, P_trap: float, alpha_loss: float, L_eff: float,
                 sigma_laser: float, sigma_mod: float, sigma_trap: float,
                 coherence_baseline: float):
        self.nu_emit = nu_emit
        self.fm = fm
        self.n_cycles = n_cycles
        self.P_in = P_in
        self.P_trap = P_trap
        self.alpha_loss = alpha_loss
        self.L_eff = L_eff
        self.sigma_laser = sigma_laser
        self.sigma_mod = sigma_mod
        self.sigma_trap = sigma_trap
        self.coherence_baseline = coherence_baseline


def compute_detuning(params: TRRParams) -> dict:
    """
    Calculate frequency shift, observed frequency, and redshift z.
    
    Args:
        params: TRR experimental parameters
        
    Returns:
        Dictionary with keys:
            - delta_nu: Frequency shift (Hz)
            - nu_obs: Observed frequency (Hz)
            - z: Redshift value (dimensionless)
    """
    delta_nu = params.n_cycles * params.fm
    nu_obs = params.nu_emit - delta_nu
    z = (params.nu_emit - nu_obs) / params.nu_emit
    return {"delta_nu": delta_nu, "nu_obs": nu_obs, "z": z}


def coupling_efficiency(params: TRRParams) -> float:
    """
    Compute trap coupling efficiency (η_c).
    
    Based on input/trap power ratio and exponential losses.
    
    Args:
        params: TRR experimental parameters
        
    Returns:
        Coupling efficiency between 0.0 and 1.0
    """
    if params.P_in <= 0:
        return 0.0
    nc = (params.P_trap / params.P_in) * np.exp(-params.alpha_loss * params.L_eff)
    return float(np.clip(nc, 0.0, 1.0))


def coherence_time(params: TRRParams) -> float:
    """
    Calculate coherence time T_c from noise sources.
    
    Combines laser, modulation, and trap noise contributions
    to determine the photon coherence time.
    
    Args:
        params: TRR experimental parameters
        
    Returns:
        Coherence time in seconds
    """
    sigma_total = np.sqrt(params.sigma_laser**2 + params.sigma_mod**2 + params.sigma_trap**2)
    norm = max(params.nu_emit, 1.0)
    Tc = params.coherence_baseline / (1.0 + (sigma_total / norm))
    return float(max(Tc, 0.0))


def escape_probability(z: float, nc: float, Tc: float, Tc_threshold: float = 1e-6) -> float:
    """
    Model photon escape probability from the optical trap.
    
    The escape probability increases with redshift magnitude,
    reduced coupling efficiency, and coherence degradation.
    
    Args:
        z: Redshift value
        nc: Coupling efficiency (0 to 1)
        Tc: Coherence time (s)
        Tc_threshold: Threshold below which coherence is critical
        
    Returns:
        Escape probability between 0.0 and 1.0
    """
    score = 2.0 * z + (1.0 - nc) + (1.0 if Tc < Tc_threshold else 0.0)
    return float(1.0 / (1.0 + np.exp(-5.0 * (score - 1.0))))


# Legacy class-based interface for backwards compatibility
class PhysicsEngine:
    """
    Legacy class-based interface for physics calculations.
    
    Note: Prefer using the standalone functions directly.
    This class is maintained for backwards compatibility.
    """
    
    @staticmethod
    def compute_detuning(params: TRRParams) -> dict:
        """Compute detuning. See compute_detuning() function."""
        return compute_detuning(params)

    @staticmethod
    def coupling_efficiency(params: TRRParams) -> float:
        """Compute coupling efficiency. See coupling_efficiency() function."""
        return coupling_efficiency(params)

    @staticmethod
    def coherence_time(params: TRRParams) -> float:
        """Compute coherence time. See coherence_time() function."""
        return coherence_time(params)

    @staticmethod
    def escape_probability(z: float, nc: float, Tc: float, Tc_threshold: float = 1e-6) -> float:
        """Compute escape probability. See escape_probability() function."""
        return escape_probability(z, nc, Tc, Tc_threshold)
