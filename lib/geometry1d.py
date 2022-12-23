def size_of_interval_union(intervals: list[tuple[int, int]]) -> int:
    """
    Compute total size of a list of intervals, each of which is assumed to include its
    endpoints. For instance, the intervals in [(-1, 2), (6, 7), (5, 10), (9, 11)]
    contain 11 total elements: -1, 0, 1, 2, 5, 6, 7, 8, 9, 10, 11.
    """
    intervals = sorted(intervals)
    bprev = -float("inf")
    size = 0
    for a, b in intervals:
        if bprev < a:
            size += b + 1 - a
            bprev = b
        elif bprev < b:
            size += b - bprev
            bprev = b
    return size
