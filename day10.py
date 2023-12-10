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


def loop_length(grid: Grid) -> int:
    def shortest_route_to(
        grid: GridDict, start: Point, end: Point, distances: dict[Point, int]
    ) -> Optional[int]:
        stack: list[Point] = [start]

        while stack:
            pos = stack.pop()
            for c in grid[pos].connections:
                if pos + c == end:
                    return distances[pos] + 1
                if pos + c in distances:
                    continue
                distances[pos + c] = distances[pos] + 1
                stack.append(pos + c)

        # Route not found
        return None

    # check each possible route from starting point separately
    for route in grid.grid[grid.start].connections:
        distances: dict[Point, int] = {grid.start: 0, grid.start + route: 1}
        cur: Point = grid.start + route
        cur_tile = grid.grid[cur]

        # replace the current tile with a version that has no link back to the start
        grid.grid[cur] = Tile(
            connections=[
                conn for conn in cur_tile.connections if cur + conn != grid.start
            ]
        )
        length: Optional[int] = shortest_route_to(
            grid.grid, start=cur, end=grid.start, distances=distances
        )
        if length is not None:
            return length

        # restore the current tile
        grid.grid[cur] = cur_tile

    assert None


def count_enclosed_tiles(grid: Grid) -> int:
    def cull_dead_ends(grid: Grid) -> GridDict:
        stack: list[Point] = [grid.start]
        visited: set[Point] = set()

        while stack:
            pos = stack[-1]

            if pos in visited:
                stack.pop()
                continue

            visited.add(pos)

            for c in grid.grid[pos].connections:
                if len(stack) > 1 and pos + c == grid.start:
                    return GridDict({p: grid.grid[p] for p in stack})
                if pos + c not in visited:
                    stack.append(pos + c)
                    break

        assert None, "No loop found"

    max_x = max(p.x for p in grid.grid.keys())
    max_y = max(p.y for p in grid.grid.keys())
    count = 0
    is_inside: bool = False

    loop_grid = cull_dead_ends(grid)

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            conns = loop_grid[Point(x, y)].connections
            if not conns:
                count += int(is_inside)
            elif Point.north() in conns:
                is_inside = not is_inside

    return count


if __name__ == "__main__":
    main()
