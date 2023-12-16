from dataclasses import dataclass
from sys import stdin
from typing import Callable

from lib import Point


def main() -> None:
    grid = Grid.from_string(stdin.read())
    start_beam = Beam(pos=Point(-1, 0), v=Point(1, 0))
    print("Part 1:", count_energized_tiles(grid, start_beam))


class GridDict(dict[Point, str]):
    def __missing__(self, key: Point) -> str:
        return "."

    @staticmethod
    def from_string(data: str) -> "GridDict":
        return GridDict(
            {
                Point(x, y): ch
                for y, line in enumerate(data.split("\n"))
                if line
                for x, ch in enumerate(line)
            }
        )


@dataclass(frozen=True)
class Grid:
    grid: GridDict
    width: int
    height: int

    @staticmethod
    def from_string(data: str) -> "Grid":
        new_grid = GridDict.from_string(data)
        max_x = max(p.x for p in new_grid.keys())
        max_y = max(p.y for p in new_grid.keys())
        return Grid(grid=new_grid, width=max_x + 1, height=max_y + 1)

    def in_bounds(self, p: Point) -> bool:
        return p.x >= 0 and p.x < self.width and p.y >= 0 and p.y < self.height


@dataclass(eq=True, frozen=True)
class Beam:
    pos: Point
    v: Point


def transform(mat: list[list[int]], vec: Point) -> Point:
    vec_: list[int] = [vec.x, vec.y]
    return Point(*[sum(a * b for a, b in zip(row, vec_)) for row in mat])


def vertical_splitter(beam_v: Point) -> list[Point]:
    # '|' splitter
    #
    # ( 0,  1) => (0, 1)
    # ( 0, -1) => (0, -1)
    # ( 1,  0) => (0, 1) & (0, -1)
    # (-1,  0) => (0, 1) & (0, -1)
    if beam_v.x == 0:
        return [beam_v]

    return [Point.north(), Point.south()]


def horizontal_splitter(beam_v: Point) -> list[Point]:
    # '-' splitter
    #
    # ( 0,  1) => (1, 0) & (-1, 0)
    # ( 0, -1) => (1, 0) & (-1, 0)
    # ( 1,  0) => (1, 0)
    # (-1,  0) => (-1, 0)
    if beam_v.y == 0:
        return [beam_v]

    return [Point.west(), Point.east()]


def left_mirror(beam_v: Point) -> list[Point]:
    # The '\' mirror can be implemented with the transformation matrix |0 1|
    #                                                                  |1 0|
    #
    # (1, 0)                ^                   | (0, 1)             (-1, 0)
    # ----> \               | (0, -1)           |                    <---- \
    #       |  (0, 1)       |                   V                          ^
    #       |               \ <----             \ ---->                    | (0, -1)
    #       V                 (-1, 0)             (1, 0)                   |
    #
    # |0 1| |1| = |0|      |0 1| |-1| = | 0|    |0 1| |0| = |1|      |0 1| | 0| = |-1|
    # |1 0| |0|   |1|      |1 0| | 0|   |-1|    |1 0| |1|   |0|      |1 0| |-1|   | 0|
    return [transform([[0, 1], [1, 0]], beam_v)]


def right_mirror(beam_v: Point) -> list[Point]:
    # The '/' mirror can be implemented with the transformation matrix | 0 -1|
    #                                                                  |-1  0|
    #
    #        ^               (-1, 0)                  | (0, 1)        (1, 0)
    #        | (0, -1)     / <----                    |              / ---->
    #        |             |                          V              ^
    #  ----> /             | (0, 1)             <---- /              | (0, -1)
    # (1, 0)               V                    (-1, 0)              |
    #
    # | 0 -1| |1| = | 0|   | 0 -1| |-1| = |0|   | 0 -1| |0| = |-1|   | 0 -1| | 0| = |1|
    # |-1  0| |0|   |-1|   |-1  0| | 0|   |1|   |-1  0| |1|   | 0|   |-1  0| |-1|   |0|
    return [transform([[0, -1], [-1, 0]], beam_v)]


def empty_space(beam_v: Point) -> list[Point]:
    return [beam_v]


TRANSFORMATIONS: dict[str, Callable[[Point], list[Point]]] = {
    "|": vertical_splitter,
    "-": horizontal_splitter,
    "\\": left_mirror,
    "/": right_mirror,
    ".": empty_space,
}


def count_energized_tiles(grid: Grid, beam: Beam) -> int:
    seen: set[Beam] = set()

    beams: list[Beam] = [beam]
    while beams:
        current: Beam = beams.pop()
        current = Beam(pos=current.pos + current.v, v=current.v)

        if not grid.in_bounds(current.pos) or current in seen:
            continue

        seen.add(current)

        beams.extend(
            Beam(pos=current.pos, v=new_v)
            for new_v in TRANSFORMATIONS[grid.grid[current.pos]](current.v)
        )

    return len(set(b.pos for b in seen))


if __name__ == "__main__":
    main()
