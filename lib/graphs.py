from queue import PriorityQueue, SimpleQueue
from collections import defaultdict
from typing import Callable, Iterable, TypeVar


V = TypeVar("V")


class NodeUnreachableError(Exception):
    ...


def shortest_paths(
    s: V,
    get_neighbors: Callable[[V], Iterable[V]],
    dist_max: int = -1,
    stop_condition: Callable[[V], bool] = lambda _: False,
) -> dict[V, int]:
    """
    Compute length of shortest path from source `s` to every other node visitable from `s`.
    If `t` is provided, stop after reaching node `t`.
    If `dist_max` is provided, only find paths of length <= dist_max.
    """
    q: SimpleQueue[V] = SimpleQueue()
    q.put(s)
    dists = {s: 0}
    while not q.empty():
        v = q.get()
        for w in get_neighbors(v):
            if w not in dists:
                dists[w] = dists[v] + 1
                if stop_condition(w):
                    return dists
                if dist_max < 0 or dists[w] < dist_max:
                    q.put(w)
    return dists


def shortest_path(s: V, t: V, get_neighbors: Callable[[V], Iterable[V]]) -> int:
    """
    Compute length of shortest path from source `s` to target `t`.
    """
    dists = shortest_paths(s, get_neighbors, stop_condition=lambda v: v == t)
    if t in dists:
        return dists[t]
    else:
        raise NodeUnreachableError(f"{t} is not reachable from {s}")


def dijkstra(s: V, get_neighbors: Callable[[V], Iterable[tuple[V, int]]]):
    q = PriorityQueue()
    q.put([0, s, False])
    q_dict = {}
    dists = defaultdict(lambda: float("inf"))
    while not q.empty():
        vdist, v, iv = q.get()
        if iv:
            continue
        for w, wcost in get_neighbors(v):
            wdist = wcost + vdist
            if wdist < dists[w]:
                dists[w] = wdist
                if w in q_dict:
                    q_dict[w][-1] = True
                entry = [wdist, w, False]
                q_dict[w] = entry
                q.put(entry)
    return dists
