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
