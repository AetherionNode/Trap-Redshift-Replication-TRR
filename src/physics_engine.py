# src/physics_engine.py

import numpy as np

class TRRParams:
    def __init__(self, nu_emit, fm, n_cycles, P_in, P_trap, alpha_loss, L_eff, sigma_laser, sigma_mod, sigma_trap, coherence_baseline):
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

class PhysicsEngine:
    @staticmethod
    def compute_detuning(params: TRRParams):
        delta_nu = params.n_cycles * params.fm
        nu_obs = params.nu_emit - delta_nu
        z = (params.nu_emit - nu_obs) / params.nu_emit
        return {"delta_nu": delta_nu, "nu_obs": nu_obs, "z": z}

    @staticmethod
    def coupling_efficiency(params: TRRParams):
        if params.P_in <= 0:
            return 0.0
        nc = (params.P_trap / params.P_in) * np.exp(-params.alpha_loss * params.L_eff)
        return float(np.clip(nc, 0.0, 1.0))

    @staticmethod
    def coherence_time(params: TRRParams):
        sigma_total = np.sqrt(params.sigma_laser**2 + params.sigma_mod**2 + params.sigma_trap**2)
        norm = max(params.nu_emit, 1.0)
        Tc = params.coherence_baseline / (1.0 + (sigma_total / norm))
        return float(max(Tc, 0.0))

    @staticmethod
    def escape_probability(z, nc, Tc, Tc_threshold=1e-6):
        score = 2.0 * z + (1.0 - nc) + (1.0 if Tc < Tc_threshold else 0.0)
        return float(1.0 / (1.0 + np.exp(-5.0 * (score - 1.0))))
