def digit_sum(n: int, b=10) -> int:
    k = 0
    while n > 0:
        k += n % b
        n //= b
    return k


def bit_sum(n: int) -> int:
    return digit_sum(n, 2)
