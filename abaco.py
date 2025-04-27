"""
abaco ~ https://github.com/starlitriver/abaco
"""
__version__ = "0.1.4"

## Chapter 0. Housekeeping.
import math, cmath, random, time
try:
    import ti_system, ti_plotlib
except ImportError: 
    pass

pi = math.pi
e = math.e


supported_characters="π α β ∞ ∑ − ± × ÷ √ ∫ © ® ∈ △ ∴ ≠ ⊆ ⊂ ⊥ ⊙ ² ³ ≤ ≥ • ∏ σ τ ∘ ⊥ ⊙"


__all__ = []

def _register(obj):
    __all__.append(obj.__name__)
    return obj



## Chapter 1. Algebra.

def q(*coefficients):
    if len(coefficients) != 3:
        raise ValueError("Needs 3 coefficients like quad(a, b, c).")

    # Unpack coefficients
    a, b, c = coefficients

    # Calculate the discriminant using cmath (it automatically handles negative discriminant)
    discriminant = cmath.sqrt(b**2 - 4*a*c) 
    discriminant = discriminant.real if discriminant.imag == 0 else discriminant

    # Calculate the roots using the quadratic formula
    root1 = (-b + discriminant) / (2*a)
    root2 = (-b - discriminant) / (2*a)

    # Check and remove the imaginary part if it's zero
    root1 = root1.real if root1.imag == 0 else root1
    root2 = root2.real if root2.imag == 0 else root2
    roots = (root1, root2)

    # Calculate the vertex
    vertex_x = -b / (2*a)
    vertex_y = (4*a*c - b**2) / (4*a)
    vertex = (vertex_x, vertex_y)

    # Root Form: f(x) = a(x - r1)(x - r2)
    if all(isinstance(root, complex) and root.imag != 0 for root in roots):
        root1 = "{} + {}j".format(root1.real, root1.imag)
        root2 = "{} + {}j".format(root2.real, root2.imag)

    # Output the results
    print("f(x) = {}x^2 + {}x + {}".format(a, b, c))
    print("  Root form ~ f(x) = {}(x - root1)(x - root2)".format(a))
    print("  Discriminant =", discriminant)
    print("  Roots =",root1,"and",root2)
    print("  TP (h,k) =", vertex)
    



def mean(*data):
    if iter(data) is data:
        data = list(data)
    return sum(data)/len(data)

def harmonic_mean(*data):
    if iter(data) is data:
        data = list(data)
    return len(data)/sum([1/x for x in data])

def median(*data):
    data = sorted(data)
    n = len(data)
    if n % 2 == 1:
        return data[n//2]
    else:
        i = n//2
        return (data[i - 1] + data[i])/2

def median_low(*data):
    data = sorted(data)
    n = len(data)
    if n % 2 == 1:
        return data[n//2]
    else:
        return data[n//2 - 1]

def median_high(*data):
    data = sorted(data)
    n = len(data)
    return data[n//2]

def median_grouped(*data, interval=1):
    data = sorted(data)
    n = len(data)
    x = data[n//2]
    L = x - interval/2
    l1 = l2 = n//2
    while (l1 > 0) and (data[l1 - 1] == x):
        l1 -= 1
    while (l2 < n) and (data[l2 + 1] == x):
        l2 += 1
    return L + (interval*(n/2 - l1)/(l2 - l1 + 1))
        
def mode(*data):
    if iter(data) is data:
        data = list(data)
    data = sorted(data)
    last = modev = None
    countmax = i = 0
    while i < len(data):
        if data[i] == last:
            count += 1
        else:
            count = 1
            last = data[i]
        if count > countmax:
            countmax = count
            modev = last
        i += 1
    return modev

def _ss(*data, c=None):
    if c is None:
        c = mean(data)
    total = total2 = 0
    for x in data:
        total += (x - c)**2
        total2 += (x - c) 
    total -= total2**2/len(data)
    return total

def variance(*data, xbar=None):
    if iter(data) is data:
        data = list(data)
    return _ss(data, xbar)/(len(data) - 1)

def pvariance(*data, mu=None):
    if iter(data) is data:
        data = list(data)
    return _ss(data, mu)/len(data)

def stdev(*data, xbar=None):
    return math.sqrt(variance(data, xbar))

def pstdev(*data, mu=None):
    return math.sqrt(pvariance(data, mu))


assert 1+1==2

print("Abaco {} is ready!".format(__version__))
