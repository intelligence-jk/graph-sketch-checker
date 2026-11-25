"""Check a claimed sketch of a polynomial graph against its exact features.

A polynomial is a list of coefficients, highest power first:
[1, -3, 2] is x^2 - 3x + 2. All arithmetic uses Fraction.
"""
from fractions import Fraction
from math import gcd


def _co(coeffs):
    c = [Fraction(x) for x in coeffs]
    while c and c[0] == 0:
        c.pop(0)
    if not c:
        raise ValueError("the zero polynomial has no graph to check")
    return c


def evaluate(coeffs, x):
    r = Fraction(0)
    for c in _co(coeffs):
        r = r * Fraction(x) + c
    return r


def derivative(coeffs):
    c = _co(coeffs)
    n = len(c) - 1
    return [c[i] * (n - i) for i in range(n)] or [Fraction(0)]


def _divisors(n):
    n = abs(n)
    return [d for d in range(1, n + 1) if n % d == 0]


def rational_roots(coeffs):
    """All rational roots, by the rational root theorem (exact)."""
    c = _co(coeffs)
    found = set()
    while len(c) > 1 and c[-1] == 0:      # root at x = 0
        found.add(Fraction(0))
        c.pop()
    if len(c) == 1:
        return sorted(found)
    lcm = 1
    for x in c:
        lcm = lcm * x.denominator // gcd(lcm, x.denominator)
    ints = [int(x * lcm) for x in c]
    for p in _divisors(ints[-1]):
        for q in _divisors(ints[0]):
            for s in (1, -1):
                r = Fraction(s * p, q)
                if evaluate(c, r) == 0:
                    found.add(r)
    return sorted(found)


def end_behaviour(coeffs):
    """(left, right) as 'up' or 'down'."""
    c = _co(coeffs)
    deg, pos = len(c) - 1, c[0] > 0
    right = "up" if pos else "down"
    left = right if deg % 2 == 0 else ("down" if pos else "up")
    return left, right


def turning_point_count(coeffs):
    """Number of turning points for degree 1 to 3 (exact via the derivative)."""
    c = _co(coeffs)
    deg = len(c) - 1
    if deg <= 1:
        return 0
    if deg == 2:
        return 1
    if deg == 3:
        a, b, cc = c[0] * 3, c[1] * 2, c[2]
        disc = b * b - 4 * a * cc
        return 2 if disc > 0 else 0
    raise ValueError("turning points are counted for degree 3 or less")


def check_sketch(coeffs, claim):
    """claim keys (all optional): y_intercept, roots, end, points.
    Returns a list of problems; an empty list means the sketch is consistent."""
    problems = []
    c = _co(coeffs)
    if "y_intercept" in claim and Fraction(claim["y_intercept"]) != c[-1]:
        problems.append(f"y-intercept should be {c[-1]}, not {claim['y_intercept']}")
    if "roots" in claim:
        claimed = {Fraction(r) for r in claim["roots"]}
        for r in sorted(claimed):
            if evaluate(c, r) != 0:
                problems.append(f"x = {r} is not on the x-axis (f = {evaluate(c, r)})")
        for r in rational_roots(c):
            if r not in claimed:
                problems.append(f"missing the x-intercept x = {r}")
    if "end" in claim and tuple(claim["end"]) != end_behaviour(c):
        problems.append(f"ends should go {end_behaviour(c)}, not {tuple(claim['end'])}")
    for x, y in claim.get("points", []):
        if evaluate(c, x) != Fraction(y):
            problems.append(f"({x}, {y}) is not on the graph; f({x}) = {evaluate(c, x)}")
    return problems
