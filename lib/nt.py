def digit_sum(n: int, b=10) -> int:
    k = 0
    while n > 0:
        k += n % b
        n //= b
    return k


def bit_sum(n: int) -> int:
    return digit_sum(n, 2)


def ext_euclidean(a: int, b: int) -> tuple[int, int, int]:
    """
    Returns a tuple (r, s, t) such that r = gcd(a, b) and such that a*s + b*t = r.
    """
    rp, r = a, b
    sp, s = 1, 0
    tp, t = 0, 1
    while r != 0:
        q = rp // r
        rp, r = r, rp - q * r
        sp, s = s, sp - q * s
        tp, t = t, tp - q * t
    return rp, sp, tp


def solve_congruences(congs: list[tuple[int, int]]) -> tuple[int, int]:
    """
    Solve a system of congruences. The argument is a list containing tuples (a, m), each
    corresponding to a congruence x = a (mod m).
    """
    a, m = congs[0]
    for b, n in congs[1:]:
        d, s, t = ext_euclidean(m, n)
        assert d == 1, "Moduli are not coprime"
        a, m = (a * t * n + b * s * m) % (m * n), m * n
    return a, m
