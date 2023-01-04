import numpy as np
from .geometry2d import Vec2


class Grid:
    """
    A 2D grid backed by a numpy array.
    """

    def __init__(self, data, wrap_vert=False, wrap_horiz=False):
        self.data = np.array(data)
        assert len(self.data.shape) == 2
        self.wrap_vert = wrap_vert
        self.wrap_horiz = wrap_horiz

    @property
    def ncols(self):
        return self.data.shape[1]

    @property
    def nrows(self):
        return self.data.shape[0]

    @property
    def rows(self):
        return self.data

    @property
    def cols(self):
        return self.data.T

    @property
    def dimensions(self):
        return Vec2(*self.data.shape)

    def __getitem__(self, key):
        return self.data[key]

    def __contains__(self, key):
        if isinstance(key, Vec2):
            return 0 <= key.x < self.nrows and 0 <= key.y < self.ncols
        else:
            return NotImplemented

    def find(self, val) -> Vec2:
        [i], [j] = np.where(self.data == val)
        return Vec2(i, j)

    def find_all(self, val) -> list[Vec2]:
        return [Vec2(i, j) for i, j in zip(*np.where(self.data == val))]

    def neighbors4(self, i: int, j: int) -> list[Vec2]:
        return [
            Vec2(i + di, j + dj)
            for di, dj in [(1, 0), (0, 1), (-1, 0), (0, -1)]
            if 0 <= i + di < self.nrows and 0 <= j + dj < self.ncols
        ]

    def neighbors8(self, i: int, j: int) -> list[Vec2]:
        return [
            Vec2(i + di, j + dj)
            for di, dj in [
                (1, 0),
                (1, 1),
                (0, 1),
                (-1, 1),
                (-1, 0),
                (-1, -1),
                (0, -1),
                (1, -1),
            ]
            if 0 <= i + di < self.nrows and 0 <= j + dj < self.ncols
        ]


class CharGrid(Grid):
    def __init__(self, data: list[str], pad: str = None):
        if pad is None:
            super().__init__([list(s) for s in data])
        else:
            width = max(len(s) for s in data)
            super().__init__([list(s.ljust(width, pad)) for s in data])

    def print_local(self, pt: Vec2, r: int, ptchar=None):
        for i in range(max(0, pt.x - r), min(self.nrows, pt.x + r)):
            print(
                "".join(
                    ptchar if ptchar and (i, j) == pt else self.data[i, j]
                    for j in range(max(0, pt.y - r), min(self.ncols, pt.y + r))
                )
            )
