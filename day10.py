from dataclasses import dataclass, field
from typing import Optional
from sys import stdin

from lib import Point, orthogonal_directions

PIPE_SYMBOLS: dict[str, list[Point]] = {
    "|": [Point.north(), Point.south()],
    "-": [Point.west(), Point.east()],
    "L": [Point.north(), Point.east()],
    "J": [Point.north(), Point.west()],
    "7": [Point.south(), Point.west()],
    "F": [Point.south(), Point.east()],
}


def main() -> None:
    grid = Grid.from_string(stdin.read())
    print("Part 1:", loop_length(grid) // 2)
    print("Part 2:", count_enclosed_tiles(grid))


@dataclass(eq=True, frozen=True)
class Tile:
    connections: list[Point] = field(default_factory=list)

    def with_connection(self, p: Point) -> "Tile":
        return Tile(connections=self.connections + [p])

    @staticmethod
    def from_string(data: str) -> "Tile":
        return Tile(connections=PIPE_SYMBOLS[data] if data in PIPE_SYMBOLS else [])


class GridDict(dict[Point, Tile]):
    def __missing__(self, key: Point) -> Tile:
        return Tile()


@dataclass(eq=True)
class Grid:
    grid: GridDict
    start: Point

    @staticmethod
    def from_string(data: str) -> "Grid":
        new_grid = GridDict()
        start = Point(0, 0)

        # Build grid
        for y, line in enumerate(data.split("\n")):
            if not line:
                continue
            for x, ch in enumerate(line):
                if ch == "S":
                    start = Point(x, y)
                new_grid[Point(x, y)] = Tile.from_string(ch)

        # Connect start point
        for p in orthogonal_directions():
            if any(p + q == Point(0, 0) for q in new_grid[start + p].connections):
                new_grid[start] = new_grid[start].with_connection(p)

        return Grid(grid=new_grid, start=start)


def cull_dead_pipes(grid: Grid) -> GridDict:
    """remove unconnected pipes from the grid, leaving only the loop"""
    visited: set[Point] = set()
    current: Optional[Point] = grid.start

    while current:
        visited.add(current)
        current = next(
            (
                current + conn
                for conn in grid.grid[current].connections
                if current + conn not in visited
            ),
            None,
        )

    return GridDict({p: grid.grid[p] for p in visited})


def loop_length(grid: Grid) -> int:
    new_grid = cull_dead_pipes(grid)
    return len(new_grid.keys())


def count_enclosed_tiles(grid: Grid) -> int:
    # We can keep track of inside/outside the loop by tracking pipes that connect north.
    # That is, when we're traversing the grid west-to-east and north-to-south, the
    # first northward connection means that we've entered inside the loop; the second
    # northward connection means we're now outside the loop, and so on. Keeping track
    # of north-connecting pipes allows us to always know if we're inside or outside of
    # the loop.
    #
    # This works only if we remove all pipes from the grid that are not part of the
    # loop.
    loop_grid = cull_dead_pipes(grid)

    # is_inner keeps track of whether we're inside or outside of the loop
    is_inner: bool = False
    inner_count: int = 0

    max_x = max(p.x for p in grid.grid.keys())
    max_y = max(p.y for p in grid.grid.keys())
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            conns = loop_grid[Point(x, y)].connections
            if not conns:
                inner_count += int(is_inner)
            elif Point.north() in conns:
                is_inner = not is_inner

    return inner_count


if __name__ == "__main__":
    main()
