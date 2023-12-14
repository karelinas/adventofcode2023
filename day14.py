from dataclasses import dataclass
from enum import IntEnum, auto
from operator import attrgetter
from sys import stdin

from lib import Point


def main() -> None:
    grid = Grid.from_string(stdin.read())
    print("Part 1:", grid.tilt().load)
    print("Part 2:", grid.n_cycles(1000000000).load)


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


def hash_grid(gd: GridDict) -> int:
    return hash(sum(hash(hash(p) + hash(t)) for p, t in gd.items()))


@dataclass(frozen=True)
class Grid:
    grid: GridDict
    width: int
    height: int

    def __str__(self) -> "str":
        string_builder = []
        reverse_map = {v: k for k, v in TILE_MAPPING.items()}
        for y in range(self.height):
            for x in range(self.width):
                string_builder.append(reverse_map[self.grid[Point(x, y)]])
            string_builder.append("\n")
        return "".join(string_builder)

    @staticmethod
    def from_string(data: str) -> "Grid":
        grid = GridDict.from_string(data)
        max_x = max(p.x for p in grid.keys())
        max_y = max(p.y for p in grid.keys())
        return Grid(grid=grid, width=max_x + 1, height=max_y + 1)

    def tilt(self, direction: Point = Point.north()) -> "Grid":
        def roll_rock(grid: GridDict, p: Point):
            while True:
                q = p + direction
                if (
                    q.y < 0
                    or q.y >= self.height
                    or q.x < 0
                    or q.x >= self.width
                    or grid[q] != Tile.Empty
                ):
                    return p
                p = q

        new_grid = GridDict({p: t for p, t in self.grid.items() if t == Tile.FixedRock})
        loose_rocks = (p for p, t in self.grid.items() if t == Tile.LooseRock)

        # west-to-east north-to-south works for north and west tilts,
        # but south and east need to be reversed
        should_reverse: bool = direction in (Point.south(), Point.east())

        for p in sorted(loose_rocks, key=attrgetter("y", "x"), reverse=should_reverse):
            new_grid[roll_rock(new_grid, p)] = Tile.LooseRock

        return Grid(grid=new_grid, width=self.width, height=self.height)

    @property
    def load(self) -> int:
        return sum(
            self.height - p.y for p, t in self.grid.items() if t == Tile.LooseRock
        )

    def cycle(self) -> "Grid":
        new_grid = self
        for direction in (Point.north(), Point.west(), Point.south(), Point.east()):
            new_grid = new_grid.tilt(direction)
        return new_grid

    def n_cycles(self, n: int) -> "Grid":
        seen: dict[int, int] = {hash_grid(self.grid): 0}
        history: dict[int, Grid] = {0: self}

        new_grid = self
        for c in range(1, n + 1):
            new_grid = new_grid.cycle()

            # detect cyclical repetition, shortcut to the end if possible
            new_hash = hash_grid(new_grid.grid)
            if new_hash in seen:
                offset = seen[new_hash]
                remainder = n - seen[new_hash]
                cycle_length = c - seen[new_hash]
                return history[offset + (remainder % cycle_length)]

            seen[new_hash] = c
            history[c] = new_grid

        return new_grid


if __name__ == "__main__":
    main()
