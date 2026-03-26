"""
Analytical solution for the Störmer problem restricted to a spherical surface.

Based on: Piña & Cortés, Eur. J. Phys. 37 (2016) 065009
"Störmer problem restricted to a spherical surface and the Euler and Lagrange tops"

The solution for theta(t) is expressed in Jacobi elliptic functions (dn or cn),
and phi(t) is obtained by numerical integration of the exact dphi/dtau expression.
"""

import numpy as np
from scipy.special import ellipj, ellipk
from scipy.integrate import cumulative_trapezoid


# ---------------------------------------------------------------------------
# Physical constants and parameters
# ---------------------------------------------------------------------------

# Default values matching sv_sphere.c and the paper (arbitrary units)
M_DEFAULT = 2.0   # mass
R_DEFAULT = 10.0  # sphere radius
K_DEFAULT = 0.5   # k = mu0 * q * m / (4 * pi * R)


def compute_constants(theta0, p_theta0, phi0, p_phi0, M=M_DEFAULT, R=R_DEFAULT, k=K_DEFAULT):
    """Compute the constants of motion and dimensionless parameters.

    Parameters
    ----------
    theta0, phi0 : float
        Initial polar and azimuthal angles.
    p_theta0, p_phi0 : float
        Initial canonical momenta (p_theta = M*R^2*theta_dot,
        p_phi = [M*R^2*phi_dot - k]*sin^2(theta)).
    M, R, k : float
        Physical parameters.

    Returns
    -------
    dict with keys: K (energy), p_phi, a, b, A, B, regime, kappa, u_dot, tau_scale
    """
    sin2 = np.sin(theta0) ** 2

    # Kinetic energy (= Hamiltonian)
    # H = (1/2MR^2) [p_theta^2 + (p_phi + k*sin^2(theta))^2 / sin^2(theta)]
    eta0 = p_phi0 + k * sin2
    K = (p_theta0**2 + eta0**2 / sin2) / (2 * M * R**2)

    if K < 1e-30:
        raise ValueError("Energy K is essentially zero — particle is stationary.")

    # Dimensionless parameters (Eq. 20)
    L = np.sqrt(2 * M * R**2 * K)  # characteristic momentum
    a = p_phi0 / L
    b = k / L

    # Discriminant (Eq. 29)
    disc = 1 - 4 * a * b
    if disc < -1e-12:
        raise ValueError(f"4ab = {4*a*b:.6f} > 1: no real motion possible.")
    disc = max(disc, 0.0)

    # Roots A, B of the quartic potential (Eqs. 26-27)
    sqrt_disc = np.sqrt(disc)
    numerator_common = 2 * b * (a + b) - 1
    A = (numerator_common - sqrt_disc) / (2 * b**2)
    B = (numerator_common + sqrt_disc) / (2 * b**2)

    # Determine regime
    if A > 1e-12:
        regime = "one_hemisphere"
        kappa = np.sqrt((B - A) / B)
        u_dot = b * np.sqrt(B)
    elif A < -1e-12:
        regime = "two_hemispheres"
        kappa = np.sqrt(B / (B - A))
        u_dot = b * np.sqrt(B - A)
    else:
        regime = "separatrix"
        kappa = 1.0
        u_dot = b * np.sqrt(B)

    # tau -> t conversion: t = tau * tau_scale
    tau_scale = np.sqrt(M * R**2 / (2 * K))

    return {
        "K": K, "p_phi": p_phi0, "a": a, "b": b,
        "A": A, "B": B, "regime": regime,
        "kappa": kappa, "u_dot": u_dot,
        "tau_scale": tau_scale, "L": L,
        "M": M, "R": R, "k": k,
    }


def _inverse_dn(y, kappa):
    """Compute u such that dn(u, kappa) = y.

    Uses dn^2 + kappa^2 * sn^2 = 1 => sn = sqrt((1 - y^2) / kappa^2).
    Then u = F(arcsin(sn), kappa) via incomplete elliptic integral.
    """
    if abs(kappa) < 1e-15:
        # dn(u, 0) = 1 for all u
        return 0.0
    sn_val = np.sqrt(np.clip((1 - y**2) / kappa**2, 0, 1))
    phi_angle = np.arcsin(np.clip(sn_val, -1, 1))
    # F(phi, kappa) — incomplete elliptic integral of the first kind
    # scipy doesn't have F directly, but we can use the relation with ellipj
    # Use numerical inversion via Newton's method
    return _invert_elliptic(lambda u: ellipj(u, kappa**2)[2], y, b_sqrt=1.0, period=2*ellipk(kappa**2))


def _inverse_cn(y, kappa):
    """Compute u such that cn(u, kappa) = y."""
    return _invert_elliptic(lambda u: ellipj(u, kappa**2)[1], y, b_sqrt=1.0, period=4*ellipk(kappa**2))


def _invert_elliptic(func, target, b_sqrt, period):
    """Find u in [0, period/2] such that func(u) = target, using bisection.

    func should be monotonically decreasing in [0, period/2].
    """
    # In the first half-period, dn decreases from 1 to sqrt(1-kappa^2)
    # and cn decreases from 1 to -1 (at half-period = 2K)
    u_lo, u_hi = 0.0, period / 2.0
    for _ in range(100):
        u_mid = (u_lo + u_hi) / 2.0
        val = func(u_mid)
        if val > target:
            u_lo = u_mid
        else:
            u_hi = u_mid
        if abs(u_hi - u_lo) < 1e-14:
            break
    return (u_lo + u_hi) / 2.0


def solve_analytical(theta0, p_theta0, phi0, p_phi0, t_final, n_points=10000,
                     M=M_DEFAULT, R=R_DEFAULT, k=K_DEFAULT):
    """Compute the analytical solution for the Störmer problem on a sphere.

    Parameters
    ----------
    theta0, phi0 : float
        Initial angles (radians).
    p_theta0, p_phi0 : float
        Initial canonical momenta.
    t_final : float
        Final time.
    n_points : int
        Number of time points.
    M, R, k : float
        Physical parameters.

    Returns
    -------
    t : ndarray of shape (n_points,)
    theta : ndarray of shape (n_points,)
    phi : ndarray of shape (n_points,)
    params : dict with computed constants
    """
    params = compute_constants(theta0, p_theta0, phi0, p_phi0, M, R, k)
    a, b = params["a"], params["b"]
    A, B = params["A"], params["B"]
    regime = params["regime"]
    kappa = params["kappa"]
    u_dot = params["u_dot"]
    tau_scale = params["tau_scale"]

    # Time arrays
    t = np.linspace(0, t_final, n_points)
    tau = t / tau_scale  # dimensionless time

    # Initial z value
    z0 = np.cos(theta0)

    if regime == "separatrix":
        raise NotImplementedError("Separatrix case (A=0) is non-periodic and not yet implemented.")

    # -------------------------------------------------------------------
    # theta(tau) via Jacobi elliptic functions
    # -------------------------------------------------------------------
    m_param = kappa**2  # scipy uses m = kappa^2

    if regime == "one_hemisphere":
        # z(tau) = sqrt(B) * dn(u_dot*tau + u0, kappa)
        # At tau=0: z0 = sqrt(B) * dn(u0, kappa)
        dn_at_0 = z0 / np.sqrt(B)
        dn_at_0 = np.clip(dn_at_0, np.sqrt(1 - m_param), 1.0)  # dn range

        # Phase offset: find u0 such that dn(u0) = dn_at_0
        if abs(dn_at_0 - 1.0) < 1e-12:
            u0 = 0.0
        else:
            u0 = _inverse_dn(dn_at_0, kappa)

        # Check sign of dz/dtau at t=0 to determine phase direction
        # dz/dtau|_{t=0} = -p_theta0 * sin(theta0) / (M*R^2) / sqrt(2K/(MR^2))
        #                 = -p_theta0 * sin(theta0) / L
        dz_dtau_0 = -p_theta0 * np.sin(theta0) / params["L"]

        # dn'(u) = -kappa^2 * sn(u) * cn(u), so dz/dtau = sqrt(B) * dn'(u) * u_dot
        # At u0: need to check if the derivative sign matches
        sn0, cn0, dn0, _ = ellipj(u0, m_param)
        dz_du = -m_param * sn0 * cn0  # dn'(u) evaluated at u0
        dz_dtau_model = np.sqrt(B) * dz_du * u_dot

        # If signs don't match, we need the other branch: u0 -> 2K - u0
        # (dn is symmetric about u=0 and has period 2K)
        if dz_dtau_0 * dz_dtau_model < -1e-15:
            period = 2 * ellipk(m_param)
            u0 = period - u0

        u = u_dot * tau + u0
        _, _, dn_vals, _ = ellipj(u, m_param)
        z = np.sqrt(B) * dn_vals

    else:  # two_hemispheres
        # z(tau) = sqrt(B) * cn(u_dot*tau + u0, kappa)
        cn_at_0 = z0 / np.sqrt(B)
        cn_at_0 = np.clip(cn_at_0, -1.0, 1.0)

        if abs(cn_at_0 - 1.0) < 1e-12:
            u0 = 0.0
        else:
            u0 = _inverse_cn(cn_at_0, kappa)

        # Check sign of dz/dtau
        dz_dtau_0 = -p_theta0 * np.sin(theta0) / params["L"]

        sn0, cn0, dn0, _ = ellipj(u0, m_param)
        dz_du = -sn0 * dn0  # cn'(u) = -sn(u)*dn(u)
        dz_dtau_model = np.sqrt(B) * dz_du * u_dot

        if dz_dtau_0 * dz_dtau_model < -1e-15:
            period = 4 * ellipk(m_param)
            u0 = period - u0

        u = u_dot * tau + u0
        _, cn_vals, _, _ = ellipj(u, m_param)
        z = np.sqrt(B) * cn_vals

    # Clamp z to [-1, 1] for safety
    z = np.clip(z, -1 + 1e-15, 1 - 1e-15)
    theta = np.arccos(z)

    # -------------------------------------------------------------------
    # phi(tau) via numerical integration of dphi/dtau = a/(1 - z^2) + b
    # -------------------------------------------------------------------
    sin2_theta = 1 - z**2
    sin2_theta = np.clip(sin2_theta, 1e-30, None)  # avoid division by zero
    dphi_dtau = a / sin2_theta + b

    # Cumulative trapezoidal integration
    phi_integral = cumulative_trapezoid(dphi_dtau, tau, initial=0.0)
    phi = phi0 + phi_integral

    return t, theta, phi, params


def to_cartesian(theta, phi, R=R_DEFAULT):
    """Convert spherical (theta, phi) to Cartesian (x, y, z)."""
    x = R * np.sin(theta) * np.cos(phi)
    y = R * np.sin(theta) * np.sin(phi)
    z = R * np.cos(theta)
    return x, y, z


def compute_energy(theta, p_theta, p_phi, M=M_DEFAULT, R=R_DEFAULT, k=K_DEFAULT):
    """Compute the Hamiltonian (should be constant)."""
    sin2 = np.sin(theta) ** 2
    eta = p_phi + k * sin2
    return (p_theta**2 + eta**2 / sin2) / (2 * M * R**2)


# ---------------------------------------------------------------------------
# Main: generate analytical solution and plots
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import os

    output_dir = os.path.join(os.path.dirname(__file__), "plots")
    os.makedirs(output_dir, exist_ok=True)

    # Physical parameters (same as sv_sphere.c)
    M, R, k = 2.0, 10.0, 0.5

    # -----------------------------------------------------------------------
    # Test cases from run.sh (matching the Störmer-Verlet simulations)
    # -----------------------------------------------------------------------
    cases = {
        "fig6a": {
            "theta0": np.pi / 4, "p_theta0": 0.0,
            "phi0": 0.0, "p_phi0": 0.394,
            "t_final": 30.0, "label": "Fig 6(a): one hemisphere",
        },
        "fig6b": {
            "theta0": np.pi / 3, "p_theta0": 0.0,
            "phi0": 0.0, "p_phi0": 0.394,
            "t_final": 3000.0, "label": "Fig 6(b): one hemisphere (long)",
        },
        "fig6c": {
            "theta0": 75 * np.pi / 180, "p_theta0": 0.0,
            "phi0": 0.0, "p_phi0": -0.394,
            "t_final": 3000.0, "label": "Fig 6(c): loops (p_phi < 0)",
        },
        "fig7a": {
            "theta0": 0.6, "p_theta0": 0.1,
            "phi0": 0.0, "p_phi0": 0.25,
            "t_final": 3000.0, "label": "Fig 7(a): one hemisphere",
        },
        "fig7c": {
            "theta0": 0.6, "p_theta0": 0.2525,
            "phi0": 0.0, "p_phi0": 0.25,
            "t_final": 3000.0, "label": "Fig 7(c): crosses equator",
        },
    }

    for name, case in cases.items():
        print(f"\n{'='*60}")
        print(f"Case: {case['label']}")
        print(f"{'='*60}")

        try:
            t, theta, phi, params = solve_analytical(
                case["theta0"], case["p_theta0"], case["phi0"], case["p_phi0"],
                case["t_final"], n_points=50000, M=M, R=R, k=k,
            )
        except (ValueError, NotImplementedError) as e:
            print(f"  Skipped: {e}")
            continue

        print(f"  Regime: {params['regime']}")
        print(f"  a = {params['a']:.6f}, b = {params['b']:.6f}")
        print(f"  A = {params['A']:.6f}, B = {params['B']:.6f}")
        print(f"  kappa = {params['kappa']:.6f}")
        print(f"  Energy K = {params['K']:.6e}")

        # Verify energy conservation
        # p_theta(t) can be recovered from dtheta/dt = dz/dtau * (-1/sin(theta)) * (1/tau_scale)
        # But for a quick check, verify z stays in expected bounds
        z = np.cos(theta)
        print(f"  z range: [{z.min():.6f}, {z.max():.6f}]")
        if params["regime"] == "one_hemisphere":
            print(f"  Expected: [{np.sqrt(params['A']):.6f}, {np.sqrt(params['B']):.6f}]")
        else:
            print(f"  Expected: [{-np.sqrt(params['B']):.6f}, {np.sqrt(params['B']):.6f}]")

        # Cartesian coordinates
        x, y, zc = to_cartesian(theta, phi, R)

        # --- 3D sphere plot ---
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(projection="3d")

        # Draw sphere
        N = 200
        u_sphere = np.linspace(0, 2 * np.pi, N)
        v_sphere = np.linspace(0, np.pi, N)
        xs = R * np.outer(np.cos(u_sphere), np.sin(v_sphere))
        ys = R * np.outer(np.sin(u_sphere), np.sin(v_sphere))
        zs = R * np.outer(np.ones(N), np.cos(v_sphere))
        ax.plot_surface(xs, ys, zs, edgecolor="#a0a0a0", lw=0.2,
                        rstride=4, cstride=4, color="#e0e0e0", alpha=0.2)

        ax.plot(x, y, zc, "-", linewidth=1.5, color="blue", label="Analytical")
        ax.set_xlim(-R, R)
        ax.set_ylim(-R, R)
        ax.set_zlim(-R, R)
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        ax.set_zlabel("$z$")
        ax.set_title(case["label"])
        ax.view_init(elev=22, azim=-48)
        plt.legend(loc="upper right", fontsize="small")
        plt.savefig(os.path.join(output_dir, f"analytical_{name}.png"), dpi=200)
        plt.close()

        # --- theta(t) plot (short window) ---
        t_window = min(case["t_final"], 100.0)
        mask = t <= t_window
        fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
        axes[0].plot(t[mask], theta[mask] * 180 / np.pi, "b-", linewidth=0.8)
        axes[0].set_ylabel(r"$\theta$ (degrees)")
        axes[0].set_title(case["label"])
        axes[0].grid(True, alpha=0.3)

        axes[1].plot(t[mask], phi[mask], "r-", linewidth=0.8)
        axes[1].set_ylabel(r"$\varphi$ (rad)")
        axes[1].set_xlabel("$t$")
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"analytical_{name}_angles.png"), dpi=200)
        plt.close()

    print(f"\nPlots saved to {output_dir}/")
