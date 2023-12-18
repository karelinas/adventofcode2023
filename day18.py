import re
from dataclasses import dataclass
from enum import IntEnum, auto
from sys import stdin

from lib import Point

RE_DIG_INSTRUCTION = re.compile(r"^([UDLR]) (\d+) \((#[0-9a-fA-F]{6})\)$")
DIG_DIRECTION_MAP: dict[str, Point] = {
    "U": Point.north(),
    "D": Point.south(),
    "L": Point.west(),
    "R": Point.east(),
}


def main() -> None:
    dig_instructions = parse_instruction(stdin.read())
    print("Part 1:", lagoon_size(dig_instructions))


@dataclass(eq=True, frozen=True)
class DigInstruction:
    direction: Point
    distance: int
    color: str

    @staticmethod
    def from_string(data: str) -> "DigInstruction":
        m = RE_DIG_INSTRUCTION.match(data)
        assert m, f"Invalid line '{data}'"

        direction, distance, color = m.groups()

        return DigInstruction(
            direction=DIG_DIRECTION_MAP[direction], distance=int(distance), color=color
        )


def parse_instruction(data: str) -> list[DigInstruction]:
    return [DigInstruction.from_string(line) for line in data.split("\n") if line]


class Tile(IntEnum):
    Ground: int = auto()
    Trench: int = auto()


class GridDict(dict[Point, Tile]):
    def __missing__(self, key: Point) -> Tile:
        return Tile.Ground


def dig_trench(trench: list[DigInstruction]) -> GridDict:
    grid = GridDict()
    pos = Point(0, 0)
    for instr in trench:
        for _ in range(instr.distance):
            grid[pos] = Tile.Trench
            pos += instr.direction
    return grid


def dig_interior(trench: GridDict) -> GridDict:
    min_x = min(p.x for p in trench.keys())
    min_y = min(p.y for p in trench.keys())
    max_x = max(p.x for p in trench.keys())
    max_y = max(p.y for p in trench.keys())

    is_inner: bool = False
    lagoon = GridDict()

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            current_tile: Tile = trench[Point(x, y)]
            north_tile: Tile = trench[Point(x, y) + Point.north()]
            if north_tile == Tile.Trench and current_tile == Tile.Trench:
                is_inner = not is_inner
            if current_tile == Tile.Trench or is_inner:
                lagoon[Point(x, y)] = Tile.Trench

    return lagoon


def lagoon_size(instructions: list[DigInstruction]) -> int:
    trench = dig_trench(instructions)
    lagoon = dig_interior(trench)
    return len(lagoon.keys())


if __name__ == "__main__":
    main()
