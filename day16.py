from dataclasses import dataclass
from sys import stdin
from typing import Callable

from lib import Point


def main() -> None:
    grid = Grid.from_string(stdin.read())
    start_beam = Beam(pos=Point(-1, 0), v=Point(1, 0))
    print("Part 1:", count_energized_tiles(grid, start_beam))
    print("Part 2:", most_energized_configuration(grid))


@dataclass(frozen=True)
class Grid:
    grid: dict[Point, str]
    width: int
    height: int

    @staticmethod
    def from_string(data: str) -> "Grid":
        new_grid = {
            Point(x, y): ch
            for y, line in enumerate(data.split("\n"))
            if line
            for x, ch in enumerate(line)
        }
        max_x = max(p.x for p in new_grid.keys())
        max_y = max(p.y for p in new_grid.keys())
        return Grid(grid=new_grid, width=max_x + 1, height=max_y + 1)

    def in_bounds(self, p: Point) -> bool:
        return p.x >= 0 and p.x < self.width and p.y >= 0 and p.y < self.height


@dataclass(eq=True, frozen=True)
class Beam:
    pos: Point
    v: Point


def matrix_transform(mat: list[list[int]], vec: Point) -> Point:
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
    return [matrix_transform([[0, 1], [1, 0]], beam_v)]


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
    return [matrix_transform([[0, -1], [-1, 0]], beam_v)]


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
        past_beam: Beam = beams.pop()
        beam = Beam(pos=past_beam.pos + past_beam.v, v=past_beam.v)

        if not grid.in_bounds(beam.pos) or beam in seen:
            # The beam is either out of the grid and continues out to infinity, or
            # it is stuck in an infinite loop. In either case, we have already seen
            # all the tiles that it will energize, so it's safe to stop simulating
            # the beam any further.
            continue

        seen.add(beam)
        tile: str = grid.grid[beam.pos]
        beams.extend(
            Beam(pos=beam.pos, v=new_v) for new_v in TRANSFORMATIONS[tile](beam.v)
        )

    return len(set(b.pos for b in seen))


def most_energized_configuration(grid: Grid) -> int:
    start_beams: list[Beam] = []

    for x in range(grid.width):
        start_beams.append(Beam(pos=Point(x, -1), v=Point.south()))
        start_beams.append(Beam(pos=Point(x, grid.height), v=Point.north()))
    for y in range(grid.height):
        start_beams.append(Beam(pos=Point(-1, y), v=Point.east()))
        start_beams.append(Beam(pos=Point(grid.width, y), v=Point.west()))

    return max(count_energized_tiles(grid, beam) for beam in start_beams)


if __name__ == "__main__":
    main()
