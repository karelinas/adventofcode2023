from dataclasses import asdict
from itertools import combinations
from sys import stdin

from lib import Point, manhattan_distance


def main() -> None:
    grid = GridDict.from_string(stdin.read())

    part1_grid = expand_universe(grid)
    print("Part 1:", sum_of_distances(part1_grid))

    part2_grid = expand_universe(grid, hubble_constant=1000000)
    print("Part 2:", sum_of_distances(part2_grid))


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
                if ch == "#"
            }
        )


def expand_universe(grid: GridDict, hubble_constant=2) -> GridDict:
    def expand_axis(grid: GridDict, axis: str) -> GridDict:
        max_coord = max(getattr(p, axis) for p in grid.keys())
        expansion: int = 0
        new_grid = GridDict()
        for coord in range(max_coord + 1):
            points = [p for p in grid.keys() if getattr(p, axis) == coord]
            if not points:
                expansion += hubble_constant - 1
            else:
                new_grid.update(
                    {
                        Point(
                            **{**asdict(p), axis: getattr(p, axis) + expansion}
                        ): grid[p]
                        for p in points
                    }
                )
        return new_grid

    expanded: GridDict = expand_axis(grid, "x")
    expanded = expand_axis(expanded, "y")
    return expanded


def sum_of_distances(grid: GridDict) -> int:
    return sum(manhattan_distance(p1, p2) for p1, p2 in combinations(grid.keys(), 2))


if __name__ == "__main__":
    main()
