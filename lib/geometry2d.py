from typing import Iterable, NamedTuple


class Vec2(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Vec2):
            sx, sy = self
            ox, oy = other
            return Vec2(sx + ox, sy + oy)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vec2):
            sx, sy = self
            ox, oy = other
            return Vec2(sx - ox, sy - oy)
        else:
            return NotImplemented

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __mul__(self, other):
        sx, sy = self
        if isinstance(other, int):
            return Vec2(sx * other, sy * other)
        elif isinstance(other, Vec2):
            ox, oy = other
            return Vec2(sx * ox, sy * oy)
        else:
            return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, int):
            sx, sy = self
            return Vec2(sx * other, sy * other)
        else:
            return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, int):
            sx, sy = self
            return Vec2(sx // other, sy // other)
        else:
            return NotImplemented

    def __mod__(self, other):
        sx, sy = self
        if isinstance(other, int):
            return Vec2(sx % other, sy % other)
        elif isinstance(other, Vec2):
            ox, oy = other
            return Vec2(sx % ox, sy % oy)
        else:
            return NotImplemented

    def neighbors4(self):
        return list(self.circle1(1))

    def neighbors8(self):
        return [
            self + d
            for d in [
                Vec2(1, 0),
                Vec2(-1, 0),
                Vec2(0, 1),
                Vec2(0, -1),
                Vec2(1, 1),
                Vec2(-1, 1),
                Vec2(1, -1),
                Vec2(-1, -1),
            ]
        ]

    def rot(self, angle: int):
        """
        Rotate this vector by an angle.
        """
        match angle % 360:
            case 0:
                return self
            case 90:
                return Vec2(-self.y, self.x)
            case 180:
                return -self
            case 270:
                return Vec2(self.y, -self.x)
        raise ValueError(f"Angle must be multiple of 90")

    def dot(self, other: "Vec2"):
        return self.x * other.x + self.y * other.y

    def norm1(self):
        """
        Get L1 norm of this vector.
        """
        return abs(self.x) + abs(self.y)

    def dist1(self, other: "Vec2"):
        """
        Get distance to another vector with respect to L1 norm.
        """
        return (self - other).norm1()

    def circle1(self, r: int):
        """
        Generate the vectors at L1 distance `r` from this vector.
        """
        if r == 0:
            yield self
        else:
            yield self + Vec2(r, 0)
            yield self - Vec2(r, 0)
            yield self + Vec2(0, r)
            yield self - Vec2(0, r)
            for dx in range(1, r):
                yield self + Vec2(dx, r - dx)
                yield self - Vec2(dx, r - dx)
                yield self + Vec2(dx, dx - r)
                yield self - Vec2(dx, dx - r)


class Box2(NamedTuple):
    xmin: int
    ymin: int
    xmax: int
    ymax: int

    @property
    def width(self):
        return self.xmax - self.xmin + 1

    @property
    def height(self):
        return self.ymax - self.ymin + 1

    @property
    def area(self):
        return self.width * self.height

    @property
    def perimeter(self):
        return 2 * (self.width + self.height)


def bounding_box2(vecs: Iterable[Vec2]) -> Box2:
    vecs_i = iter(vecs)
    xmin, ymin = next(vecs_i)
    xmax, ymax = xmin, ymin
    for x, y in vecs_i:
        if x < xmin:
            xmin = x
        elif x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        elif y > ymax:
            ymax = y
    return Box2(xmin, ymin, xmax, ymax)
