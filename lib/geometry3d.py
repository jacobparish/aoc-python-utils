from .geometry2d import Vec2
from typing import Iterable, NamedTuple


class Vec3(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        if isinstance(other, Vec3):
            sx, sy, sz = self
            ox, oy, oz = other
            return Vec3(sx + ox, sy + oy, sz + oz)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vec3):
            sx, sy, sz = self
            ox, oy, oz = other
            return Vec3(sx - ox, sy - oy, sz - oz)
        else:
            return NotImplemented

    def __neg__(self):
        return Vec2(-self.x, -self.y, -self.z)

    def __mul__(self, other):
        sx, sy, sz = self
        if isinstance(other, int):
            return Vec3(sx * other, sy * other, sz * other)
        elif isinstance(other, Vec3):
            ox, oy, oz = other
            return Vec3(sx * ox, sy * oy, sz * oz)
        else:
            return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, int):
            sx, sy, sz = self
            return Vec3(sx * other, sy * other, sz * other)
        else:
            return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, int):
            sx, sy, sz = self
            return Vec3(sx // other, sy // other, sz // other)
        else:
            return NotImplemented

    def __mod__(self, other):
        sx, sy, sz = self
        if isinstance(other, int):
            return Vec3(sx % other, sy % other, sz % other)
        elif isinstance(other, Vec3):
            ox, oy, oz = other
            return Vec3(sx % ox, sy % oy, sz % oz)
        else:
            return NotImplemented

    def neighbors6(self):
        return [
            self + d
            for d in [
                Vec3(1, 0, 0),
                Vec3(-1, 0, 0),
                Vec3(0, 1, 0),
                Vec3(0, -1, 0),
                Vec3(0, 0, 1),
                Vec3(0, 0, -1),
            ]
        ]

    def xy(self):
        """
        Get projection of this vector onto the xy-plane.
        """
        return Vec2(self.x, self.y)

    def xz(self):
        """
        Get projection of this vector onto the xz-plane.
        """
        return Vec2(self.x, self.z)

    def yz(self):
        """
        Get projection of this vector onto the yz-plane.
        """
        return Vec2(self.y, self.z)

    def rot_x(self, angle: int):
        """
        Rotate about the x-axis.
        """
        y, z = self.yz().rot(angle)
        Vec3(self.x, y, z)

    def rot_y(self, angle: int):
        """
        Rotate about the y-axis.
        """
        x, z = self.xz().rot(angle)
        Vec3(x, self.y, z)

    def rot_z(self, angle: int):
        """
        Rotate about the z-axis.
        """
        x, y = self.xy().rot(angle)
        Vec3(x, y, self.z)

    def dot(self, other: "Vec3"):
        """
        Get dot product of this vector with another vector.
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def norm1(self):
        """
        Return L1 norm.
        """
        return abs(self.x) + abs(self.y) + abs(self.z)

    def dist1(self, other: "Vec3"):
        """
        Return distance to another Vec3 with respect to L1 norm.
        """
        return (self - other).norm1()


class Box3(NamedTuple):
    xmin: int
    ymin: int
    xmax: int
    ymax: int
    zmin: int
    zmax: int

    @property
    def width(self):
        return self.xmax - self.xmin + 1

    @property
    def height(self):
        return self.ymax - self.ymin + 1

    @property
    def depth(self):
        return self.zmax - self.zmin + 1

    @property
    def volume(self):
        return self.width * self.height * self.depth

    @property
    def surface_area(self):
        return 2 * (
            self.width * self.height
            + self.width * self.depth
            + self.height * self.depth
        )


def bounding_box3(vecs: Iterable[Vec3]) -> Box3:
    vecs_i = iter(vecs)
    xmin, ymin, zmin = next(vecs_i)
    xmax, ymax, zmax = xmin, ymin, zmin
    for x, y, z in vecs_i:
        if x < xmin:
            xmin = x
        elif x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        elif y > ymax:
            ymax = y
        if z < zmin:
            zmin = z
        elif z > zmax:
            zmax = z
    return Box3(xmin, ymin, xmax, ymax, zmin, zmax)
