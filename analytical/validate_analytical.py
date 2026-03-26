"""
Validate the analytical solution by comparing with the Störmer-Verlet integrator.

Runs sv_sphere.c for several test cases and compares theta(t) and phi(t)
with the analytical Jacobi elliptic function solution.
"""

import subprocess
import os
import numpy as np
import matplotlib.pyplot as plt
from stormer_sphere_analytical import solve_analytical, to_cartesian

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SV_DIR = os.path.join(SCRIPT_DIR, "..", "simulation", "constraint_case", "sphere")
SV_BIN = os.path.join(SV_DIR, "sv")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "plots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Physical parameters (matching sv_sphere.c)
M, R, k = 2.0, 10.0, 0.5


def run_stormer_verlet(t_final, theta0, p_theta0, phi0, p_phi0):
    """Run the C Störmer-Verlet integrator and parse output."""
    particle_file = os.path.join(SV_DIR, "data", "validate_particle.dat")
    phase_file = os.path.join(SV_DIR, "data", "validate_phase.dat")

    cmd = [SV_BIN, str(t_final), str(theta0), str(p_theta0),
           str(phi0), str(p_phi0), particle_file, phase_file]
    subprocess.run(cmd, check=True, capture_output=True)

    # Parse particle data (n x y z)
    data = np.loadtxt(particle_file, skiprows=1)
    n_steps = data[:, 0].astype(int)
    x_sv, y_sv, z_sv = data[:, 1], data[:, 2], data[:, 3]

    dt = 0.0002  # from sv_sphere.c
    t_sv = n_steps * dt

    # Convert back to spherical
    r_sv = np.sqrt(x_sv**2 + y_sv**2 + z_sv**2)
    theta_sv = np.arccos(z_sv / r_sv)
    phi_sv = np.arctan2(y_sv, x_sv)

    # Unwrap phi for continuity
    phi_sv = np.unwrap(phi_sv)

    return t_sv, theta_sv, phi_sv, x_sv, y_sv, z_sv


def validate_ode_residual(t, theta, phi, params):
    """Check that z_dot^2 = b^2 * (B - z^2) * (z^2 - A) holds."""
    a_p, b_p = params["a"], params["b"]
    A, B = params["A"], params["B"]
    tau_scale = params["tau_scale"]

    z = np.cos(theta)
    tau = t / tau_scale

    # Numerical derivative of z w.r.t. tau
    dz_dtau = np.gradient(z, tau, edge_order=2)

    # LHS: (dz/dtau)^2
    lhs = dz_dtau**2

    # RHS: b^2 * (B - z^2) * (z^2 - A)
    rhs = b_p**2 * (B - z**2) * (z**2 - A)

    # Avoid edges where gradient is noisy
    interior = slice(10, -10)
    residual = np.abs(lhs[interior] - rhs[interior])

    return residual.mean(), residual.max()


# Test cases
cases = [
    {
        "name": "fig6b_one_hemi",
        "theta0": np.pi / 3, "p_theta0": 0.0,
        "phi0": 0.0, "p_phi0": 0.394,
        "t_final": 100.0,
        "label": "One hemisphere ($\\theta_0=60°$, $p_\\varphi=0.394$)",
    },
    {
        "name": "fig6c_loops",
        "theta0": 75 * np.pi / 180, "p_theta0": 0.0,
        "phi0": 0.0, "p_phi0": -0.394,
        "t_final": 100.0,
        "label": "Loops ($\\theta_0=75°$, $p_\\varphi=-0.394$)",
    },
    {
        "name": "fig7a_hemi",
        "theta0": 0.6, "p_theta0": 0.1,
        "phi0": 0.0, "p_phi0": 0.25,
        "t_final": 100.0,
        "label": "One hemisphere ($\\theta_0=0.6$, $p_\\theta=0.1$, $p_\\varphi=0.25$)",
    },
    {
        "name": "fig7c_cross",
        "theta0": 0.6, "p_theta0": 0.2525,
        "phi0": 0.0, "p_phi0": 0.25,
        "t_final": 100.0,
        "label": "Crosses equator ($\\theta_0=0.6$, $p_\\theta=0.2525$, $p_\\varphi=0.25$)",
    },
]

print("=" * 70)
print("VALIDATION: Analytical vs Störmer-Verlet")
print("=" * 70)

for case in cases:
    name = case["name"]
    print(f"\n--- {case['label']} ---")

    # Analytical solution
    t_an, theta_an, phi_an, params = solve_analytical(
        case["theta0"], case["p_theta0"], case["phi0"], case["p_phi0"],
        case["t_final"], n_points=50000, M=M, R=R, k=k,
    )

    # Störmer-Verlet
    t_sv, theta_sv, phi_sv_raw, x_sv, y_sv, z_sv = run_stormer_verlet(
        case["t_final"], case["theta0"], case["p_theta0"],
        case["phi0"], case["p_phi0"],
    )

    # Interpolate analytical to SV time grid for comparison
    theta_an_interp = np.interp(t_sv, t_an, theta_an)
    phi_an_interp = np.interp(t_sv, t_an, phi_an)

    # Errors
    theta_err = np.abs(theta_an_interp - theta_sv)
    # For phi, compare modulo 2*pi drift — use the difference
    phi_err = np.abs(phi_an_interp - phi_sv_raw)

    print(f"  Regime: {params['regime']}")
    print(f"  a = {params['a']:.6f}, b = {params['b']:.6f}")
    print(f"  A = {params['A']:.6f}, B = {params['B']:.6f}")
    print(f"  theta error: mean={theta_err.mean():.2e}, max={theta_err.max():.2e}")
    print(f"  phi error:   mean={phi_err.mean():.2e}, max={phi_err.max():.2e}")

    # ODE residual check
    res_mean, res_max = validate_ode_residual(t_an, theta_an, phi_an, params)
    print(f"  ODE residual (z_dot^2 vs b^2*(B-z^2)*(z^2-A)): mean={res_mean:.2e}, max={res_max:.2e}")

    # --- Comparison plots ---
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # theta comparison
    axes[0].plot(t_sv, theta_sv * 180 / np.pi, "b-", linewidth=0.8, label="Störmer-Verlet")
    axes[0].plot(t_an, theta_an * 180 / np.pi, "r--", linewidth=0.8, label="Analytical")
    axes[0].set_ylabel(r"$\theta$ (deg)")
    axes[0].legend()
    axes[0].set_title(case["label"])
    axes[0].grid(True, alpha=0.3)

    # phi comparison
    axes[1].plot(t_sv, phi_sv_raw, "b-", linewidth=0.8, label="Störmer-Verlet")
    axes[1].plot(t_an, phi_an, "r--", linewidth=0.8, label="Analytical")
    axes[1].set_ylabel(r"$\varphi$ (rad)")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    # errors
    axes[2].semilogy(t_sv, theta_err, "b-", linewidth=0.8, label=r"$|\Delta\theta|$")
    axes[2].semilogy(t_sv, phi_err, "r-", linewidth=0.8, label=r"$|\Delta\varphi|$")
    axes[2].set_ylabel("Absolute error")
    axes[2].set_xlabel("$t$")
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"validation_{name}.png"), dpi=200)
    plt.close()

    # 3D comparison
    x_an, y_an, z_an = to_cartesian(theta_an, phi_an, R)

    fig = plt.figure(figsize=(10, 5))

    ax1 = fig.add_subplot(121, projection="3d")
    ax1.plot(x_sv, y_sv, z_sv, "b-", linewidth=1, label="Störmer-Verlet")
    ax1.set_title("Störmer-Verlet")
    ax1.set_xlim(-R, R); ax1.set_ylim(-R, R); ax1.set_zlim(-R, R)
    ax1.view_init(elev=22, azim=-48)

    ax2 = fig.add_subplot(122, projection="3d")
    ax2.plot(x_an, y_an, z_an, "r-", linewidth=1, label="Analytical")
    ax2.set_title("Analytical")
    ax2.set_xlim(-R, R); ax2.set_ylim(-R, R); ax2.set_zlim(-R, R)
    ax2.view_init(elev=22, azim=-48)

    fig.suptitle(case["label"], fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"validation_3d_{name}.png"), dpi=200)
    plt.close()

print(f"\nValidation plots saved to {OUTPUT_DIR}/")
