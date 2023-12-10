from dataclasses import dataclass
from typing import Iterator


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, rhs: "Point") -> "Point":
        return Point(x=self.x + rhs.x, y=self.y + rhs.y)

    def __sub__(self, rhs: "Point") -> "Point":
        return Point(x=self.x - rhs.x, y=self.y - rhs.y)

    def reverse(self) -> "Point":
        return Point(-self.x, -self.y)

    @staticmethod
    def north() -> "Point":
        return Point(0, -1)

    @staticmethod
    def south() -> "Point":
        return Point(0, 1)

    @staticmethod
    def west() -> "Point":
        return Point(-1, 0)

    @staticmethod
    def east() -> "Point":
        return Point(1, 0)

    @staticmethod
    def northwest() -> "Point":
        return Point(-1, -1)

    @staticmethod
    def northeast() -> "Point":
        return Point(1, -1)

    @staticmethod
    def southwest() -> "Point":
        return Point(-1, 1)

    @staticmethod
    def southeast() -> "Point":
        return Point(1, 1)


def adjacent_directions() -> list[Point]:
    return [
        Point.northwest(),
        Point.north(),
        Point.northeast(),
        Point.west(),
        Point.east(),
        Point.southwest(),
        Point.south(),
        Point.southeast(),
    ]


def neighborhood(p: Point) -> Iterator[Point]:
    return (p + d for d in adjacent_directions())


def orthogonal_directions() -> list[Point]:
    return [
        Point.north(),
        Point.west(),
        Point.east(),
        Point.south(),
    ]


def orthogonal_neighborhood(p: Point) -> Iterator[Point]:
    return (p + d for d in orthogonal_directions())
