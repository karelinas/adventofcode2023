from dataclasses import dataclass
from sys import stdin

from lib import Point, orthogonal_neighborhood


def main() -> None:
    grid = Grid.from_string(stdin.read())
    print("Part 1:", count_plots_reachable_in_n_steps(grid, n=64))
    print("Part 2:", interpolate_plots_reachable_in_n_steps(grid, n=26501365))


class GridDict(dict[Point, str]):
    def __missing__(self, key: Point) -> str:
        return "."


@dataclass
class Grid:
    grid: GridDict
    start: Point

    width: int
    height: int

    @staticmethod
    def from_string(data: str) -> "Grid":
        grid = GridDict(
            {
                Point(x, y): ch
                for y, line in enumerate(data.split("\n"))
                if line
                for x, ch in enumerate(line)
            }
        )
        start: Point = next(k for k, v in grid.items() if v == "S")
        grid[start] = "."

        max_x = max(p.x for p in grid.keys())
        max_y = max(p.y for p in grid.keys())

        return Grid(grid=grid, start=start, width=max_x + 1, height=max_y + 1)

    def __getitem__(self, key: Point) -> str:
        p = Point(key.x % self.width, key.y % self.height)
        return self.grid[p]


def count_plots_reachable_in_n_steps(grid: Grid, n: int) -> int:
    locations: set[Point] = set([grid.start])
    for step in range(1, n + 1):
        new_locations = set(
            neighbor
            for pos in locations
            for neighbor in orthogonal_neighborhood(pos)
            if grid[neighbor] != "#"
        )
        locations = new_locations

    return len(locations)


def interpolate_plots_reachable_in_n_steps(grid: Grid, n: int) -> int:
    assert grid.start.x == grid.start.x
    assert grid.height == grid.width

    offset = n % grid.height
    ys = [
        count_plots_reachable_in_n_steps(grid, offset),
        count_plots_reachable_in_n_steps(grid, offset + grid.height),
        count_plots_reachable_in_n_steps(grid, offset + grid.height * 2),
    ]

    # interpolate quadratic equation
    a = (ys[0] + ys[2] - 2 * ys[1]) / 2
    b = ys[1] - ys[0] - a
    c = ys[0]
    goal = n // grid.height
    return int(a * goal**2 + b * goal + c)


if __name__ == "__main__":
    main()
