from math import *
def f(x):
    return float(1/x+sin(x))

a=1
b=4

def bisect(tolerance=0.0001, max_iterations=100):
    global a,b
    a=float(a)
    b=float(b)
    # Initial setup and validation
    print("Interval [a,b] is [%.1f, %.1f], Tolerance: %f, Max Iter: %d" % (a, b, tolerance, max_iterations))
    print()

    fa = f(a)
    fb = f(b)

    # Ensure the function has opposite signs at the endpoints
    if fa * fb >= 0:
        print("Error: Function must have opposite signs at interval endpoints.")
        print("f(%.6f) = %.6f" % (a, fa))
        print("f(%.6f) = %.6f" % (b, fb))
        return

    # Initialize variables for the iteration loop
    current_a = a
    current_b = b
    iteration_count = -1

    # Initial midpoint and function value at midpoint for first row
    m_init = (current_a + current_b) / 2
    fm_init = f(m_init)

    # Print table header
    print("%-8s %-8s %-8s %-8s %-8s %-8s %-8s" % ("Pass", "a", "m", "b", "f(a)", "f(m)", "f(b)"))
    print()

    # Start the bisection iteration loop
    while (current_b - current_a) / 2 > tolerance and iteration_count < max_iterations:
        iteration_count += 1
        root_approx = (current_a + current_b) / 2
        f_mid = f(root_approx)
        f_current_a = f(current_a)
        f_current_b = f(current_b)

        # Print the details of the current iteration
        print("%-8d %-10.4f %-10.4f %-10.4f %-12.6f %-12.6f %-12.6f" % \
              (iteration_count, current_a, root_approx, current_b, f_current_a, f_mid, f_current_b))

        # Update the interval based on the sign of f(m)
        if f_current_a * f_mid < 0:
            current_b = root_approx
        else:
            current_a = root_approx

    # Final results
    print()
    final_approx = (current_a + current_b) / 2
    if (current_b - current_a) / 2 <= tolerance:
        print("Method converged successfully to tolerance %f in %d iterations." % (tolerance, iteration_count))
    else:
        print("Maximum iterations (%d) reached before achieving tolerance %f." % (max_iterations, tolerance))

    print("Approximate root is: %.6f" % final_approx)
    print("Function value at approx: f(%.6f) = %.6f" % (final_approx, f(final_approx)))
    print("Final interval: [%.6f, %.6f]" % (current_a, current_b))
    print("Final interval width: %.6f" % (current_b - current_a))

bisect()
