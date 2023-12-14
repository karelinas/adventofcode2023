from dataclasses import dataclass
from enum import IntEnum, auto
from functools import cmp_to_key
from sys import stdin

from lib import Point


def main() -> None:
    grid = Grid.from_string(stdin.read())
    grid = grid.tilt()
    print("Part 1:", grid.load())


class Tile(IntEnum):
    Empty: int = auto()
    LooseRock: int = auto()
    FixedRock: int = auto()


TILE_MAPPING: dict[str, Tile] = {
    ".": Tile.Empty,
    "O": Tile.LooseRock,
    "#": Tile.FixedRock,
}


class GridDict(dict[Point, Tile]):
    def __missing__(self, key: Point) -> Tile:
        return Tile.Empty

    @staticmethod
    def from_string(data: str) -> "GridDict":
        return GridDict(
            {
                Point(x, y): TILE_MAPPING[ch]
                for y, line in enumerate(data.split("\n"))
                if line
                for x, ch in enumerate(line)
                if ch != "."
            }
        )


@dataclass(frozen=True)
class Grid:
    grid: GridDict
    width: int
    height: int

    @staticmethod
    def from_string(data: str) -> "Grid":
        grid = GridDict.from_string(data)
        max_x = max(p.x for p in grid.keys())
        max_y = max(p.y for p in grid.keys())
        return Grid(grid=grid, width=max_x + 1, height=max_y + 1)

    def tilt(self) -> "Grid":
        def grid_order_point_cmp(p1: Point, p2: Point):
            if p1.y < p2.y:
                return -1
            if p1.y > p2.y:
                return 1
            if p1.x < p2.x:
                return -1
            if p1.x > p2.x:
                return 1
            return 0

        def roll_rock(grid: GridDict, p: Point):
            while True:
                if p.y == 0 or grid[p + Point.north()] != Tile.Empty:
                    return p
                p = p + Point.north()

        new_grid = GridDict({p: t for p, t in self.grid.items() if t == Tile.FixedRock})
        loose_rocks = (p for p, t in self.grid.items() if t == Tile.LooseRock)
        for p in sorted(loose_rocks, key=cmp_to_key(grid_order_point_cmp)):
            new_grid[roll_rock(new_grid, p)] = Tile.LooseRock

        return Grid(grid=new_grid, width=self.width, height=self.height)

    def load(self) -> int:
        return sum(
            self.height - p.y for p, t in self.grid.items() if t == Tile.LooseRock
        )


if __name__ == "__main__":
    main()
