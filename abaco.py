"""
abaco  –  Analytical & Basic Assistant for Calculus Operations
Version: 0.1.1   •   Updated: 2025‑04‑26
Author : <your name>

A lightweight, exam‑safe MicroPython helper library for VCE Mathematical Methods
and Specialist Mathematics on the TI‑Nspire CX II.

Usage (on calc):
    from abaco import *
    help()          # overview
    help('calc')    # calculus helpers
"""

# ── Standard + TI‑specific modules ─────────────────────────
import math, cmath, random, time
import ti_system, ti_plotlib, ti_draw, ti_image, ti_hub, ti_rover

# Expose imported modules to users of `abaco`
__all__ = [
    'math', 'cmath', 'random', 'time',
    'ti_system', 'ti_plotlib', 'ti_draw', 'ti_image', 'ti_hub', 'ti_rover'
]

# ── Internal helper to auto‑register library symbols ───────

def _register(obj):
    """Decorator: add obj.__name__ to __all__ and return obj"""
    __all__.append(obj.__name__)
    return obj

# ── Utils ──────────────────────────────────────────────────
@_register
def ver():
    """Return Abaco version string."""
    return "0.1.1"

# ── Calculus ───────────────────────────────────────────────
@_register
def diff(f, x, h=1e-6):
    """Numerical derivative f'(x) using a central difference."""
    return (f(x + h) - f(x - h)) / (2 * h)

@_register
def nint(f, a, b, n=1000):
    """Trapezoidal estimate of the definite integral ∫_a^b f(x) dx."""
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return s * h

# ── Algebra ────────────────────────────────────────────────
@_register
def quad(a, b, c):
    """Return roots of ax²+bx+c=0 and discriminant as (r1, r2, disc)."""
    disc = b * b - 4 * a * c
    if disc < 0:
        return None
    d = math.sqrt(disc)
    return ((-b + d) / (2 * a), (-b - d) / (2 * a), disc)

# ── Mini‑help system ───────────────────────────────────────

def help(topic=None):
    """Quick help on Abaco topics."""
    if topic is None:
        print("abaco topics: utils, calc, alg")
        print("call help('calc') for calculus helpers")
    else:
        t = topic.lower()
        if t in ('calc', 'calculus'):
            print("diff, nint")
        elif t in ('alg', 'algebra'):
            print("quad")
        else:
            print("topic not found")

# ── Self‑test ──────────────────────────────────────────────

def _self_test():
    assert abs(diff(lambda x: x**3, 2) - 12) < 1e-3
    assert abs(nint(math.sin, 0, math.pi, 10000) - 2) < 1e-3
    assert quad(1, -5, 6)[0] == 3
    print("Self‑test OK")

