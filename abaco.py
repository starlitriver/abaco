"""
abaco  –  Analytical & Basic Assistant for Calculus Operations
Version: 0.1.1   •   Updated: 2025‑04‑26
Author : <your name>

A lightweight, exam‑safe MicroPython helper library for VCE Mathematical Methods
and Specialist Mathematics on the TI‑Nspire CX II.

Usage (on calc):
    from abaco import *
    help()              # overview
    help('calc')        # calculus helpers

Sections
--------
    utils       – small generic helpers
    algebra     – quadratic roots, factorisation, ...
    calculus    – numeric diff/integrate, bisection, Newton solve, ...
    geometry    – vectors, dot/cross, angle between, ...
    stats       – mean, stdev, normal_cdf, ...
    _self_test  – quick regression tests (ignored in exam)

Implementation notes
--------------------
• Keep functions micro‑friendly: primitive types, no list comps >100k.
• Docstrings are stripped by the build script when pushing to calc.
• All public symbols are autocollected into __all__ by @_register.
"""

# ── Standard + TI‑specific module imports ───────────────────────────────────
import math, cmath, random, time

# Attempt to import TI‑Nspire specific modules; tolerate desktop failures
try:
    import ti_system
except ImportError:  # running off‑calc
    ti_system = None  # type: ignore

try:
    import ti_plotlib
except ImportError:
    ti_plotlib = None  # type: ignore

__version__ = "0.1.2"
__all__ = []

# internal decorator to auto‑register public API

def _register(obj):
    __all__.append(obj.__name__)
    return obj


# ───────────────────────────────── utils ──────────────────────────────────────
@_register
def safe_div(a, b, default=None):
    """Return a / b, or *default* if b == 0 (default: None)."""
    try:
        return a / b
    except ZeroDivisionError:
        return default


# ─────────────────────────────── algebra ─────────────────────────────────────
@_register
def quad(a: float, b: float, c: float):
    """
    quad_info(a, b, c) → dict

    Returns every key fact about y = ax² + bx + c:
        • 'axis'         – x-coordinate of axis of symmetry
        • 'disc'         – discriminant (∆)
        • 'roots'        – tuple of real/complex roots (r1, r2)  (None if a = 0)
        • 'vertex'       – (x_v, y_v) coordinates of the vertex
    """
    if a == 0:
        return {
            'axis': None,
            'disc': None,
            'roots': None,
            'vertex': None,
        }

    axis = -b / (2 * a)
    disc = b * b - 4 * a * c
    # complex support works fine on-calc (cmath not needed for basic √ of negative)
    root_disc = disc**0.5 if disc >= 0 else (-disc)**0.5 * 1j
    r1 = (-b + root_disc) / (2 * a)
    r2 = (-b - root_disc) / (2 * a)
    y_v = a * axis * axis + b * axis + c

    return {
        'axis': axis,
        'disc': disc,
        'roots': (r1, r2),
        'vertex': (axis, y_v),
    }
# ────────────────────────────── calculus ─────────────────────────────────────
@_register
def diff(f, x, h=1e-4):
    """Central difference derivative f'(x)."""
    return (f(x + h) - f(x - h)) / (2 * h)


@_register
def nint(f, a, b, n=500):
    """
    Trapezoidal numeric integral of f from a to b using n sub‑intervals.
    """
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return s * h


@_register
def bisection(f, a, b, tol=1e-6, iters=50, track=False):
    """
    Bisection root finder for continuous f on [a, b] where f(a) and f(b) have
    opposite signs.

    Args:
        f (callable): function whose root is sought.
        a, b (float): interval endpoints.
        tol (float) : stop when |b - a| < tol or |f(mid)| < tol.
        iters (int) : maximum iterations.
        track (bool): if True, return a list of (lo, hi, mid, f(mid)) per step;
                      if False, return the final root approximation only.

    Returns:
        float or list or None: root approximation, list of steps, or None if
        the initial interval does not bracket a root.
    """
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        return None

    steps = []
    lo, hi = a, b
    for _ in range(iters):
        mid = (lo + hi) / 2
        fmid = f(mid)
        if track:
            steps.append((lo, hi, mid, fmid))

        if abs(fmid) < tol or (hi - lo) / 2 < tol:
            return steps if track else mid

        if fa * fmid < 0:
            hi, fb = mid, fmid
        else:
            lo, fa = mid, fmid

    # Reached iteration limit
    return steps if track else (lo + hi) / 2


@_register
def newton(f, dfdx, x0, tol=1e-6, iters=20):
    """
    Newton–Raphson root finder. Returns approximate root or None if diverged.
    """
    x = x0
    for _ in range(iters):
        y = f(x)
        if abs(y) < tol:
            return x
        d = dfdx(x)
        if d == 0:
            break
        x -= y / d
    return None


# ────────────────────────────── geometry ─────────────────────────────────────
@_register
def dot(u, v):
    """Dot product of 2‑ or 3‑vector tuples."""
    return sum(ua * va for ua, va in zip(u, v))


@_register
def cross(u, v):
    """Cross product of 3‑vector tuples."""
    ux, uy, uz = u
    vx, vy, vz = v
    return (
        uy * vz - uz * vy,
        uz * vx - ux * vz,
        ux * vy - uy * vx,
    )


# ─────────────────────────────── stats ───────────────────────────────────────
@_register
def mean(data):
    return sum(data) / len(data)


@_register
def stdev(data):
    mu = mean(data)
    return (sum((x - mu) ** 2 for x in data) / (len(data) - 1)) ** 0.5


# ──────────────────────────── self‑test ──────────────────────────────────────

def _self_test():
    assert quad(1, -3, 2)[:2] == (2.0, 1.0)
    assert abs(diff(lambda t: t**2, 3) - 6) < 1e-2
    assert abs(nint(lambda t: t, 0, 1) - 0.5) < 1e-3
    assert abs(bisection(lambda x: x - 2, 0, 5) - 2) < 1e-6
    v = (1, 2, 3)
    assert dot(v, v) == 14
    print("✔ abaco self‑test passed")


if __name__ == "__main__":
    _self_test()
