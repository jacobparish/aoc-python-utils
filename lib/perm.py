def invert_perm(perm: list[int]) -> list[int]:
    """
    Invert a permutation, e.g. invert_perm([1,2,0,4,3]) = [2,0,1,4,3].
    """
    inv = [None] * len(perm)
    for i, j in enumerate(perm):
        assert inv[j] is None, f"Not a permutation, {i} and {inv[j]} both map to {j}"
        inv[j] = i
    return inv
