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


def neighborhood(p: Point) -> Iterator[Point]:
    return (
        p + d
        for d in (
            Point(-1, -1),
            Point(0, -1),
            Point(1, -1),
            Point(-1, 0),
            Point(1, 0),
            Point(-1, 1),
            Point(0, 1),
            Point(1, 1),
        )
    )
