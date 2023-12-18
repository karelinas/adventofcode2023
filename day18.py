import re
from dataclasses import dataclass
from enum import IntEnum, auto
from operator import attrgetter
from sys import stdin
from typing import Optional

from lib import Point

RE_DIG_INSTRUCTION = re.compile(r"^([UDLR]) (\d+) \(#([0-9a-fA-F]{6})\)$")
DIG_DIRECTION_MAP: dict[str, Point] = {
    "U": Point.north(),
    "D": Point.south(),
    "L": Point.west(),
    "R": Point.east(),
}
SWAPPED_DIG_DIRECTION_MAP: dict[str, Point] = {
    "0": Point.east(),
    "1": Point.south(),
    "2": Point.west(),
    "3": Point.north(),
}


def main() -> None:
    dig_instructions = parse_instruction(stdin.read())
    print("Part 1:", lagoon_size(dig_instructions))
    swapped = swap_instructions(dig_instructions)
    print("Part 2:", lagoon_size(swapped))


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

    def swap(self) -> "DigInstruction":
        swapped_direction = SWAPPED_DIG_DIRECTION_MAP[self.color[5]]
        swapped_distance = int(self.color[:5], base=16)
        return DigInstruction(
            direction=swapped_direction, distance=swapped_distance, color=self.color
        )


def parse_instruction(data: str) -> list[DigInstruction]:
    return [DigInstruction.from_string(line) for line in data.split("\n") if line]


def swap_instructions(instructions: list[DigInstruction]) -> list[DigInstruction]:
    return [inst.swap() for inst in instructions]


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


def lagoon_size(instructions: list[DigInstruction]) -> int:
    trench = dig_trench(instructions)

    lagoon_size: int = 0
    left_wall: Optional[Point] = None

    for p in sorted(trench.keys(), key=attrgetter("y", "x")):
        current_tile: Tile = trench[p]
        north_tile: Tile = trench[p + Point.north()]

        if north_tile != Tile.Trench or current_tile != Tile.Trench:
            if current_tile == Tile.Trench and left_wall:
                # we'll add the trenches back in later, so make sure
                # we don't add them twice here
                lagoon_size -= 1

            continue

        if left_wall:
            lagoon_size += p.x - left_wall.x - 1
            left_wall = None
        else:
            left_wall = p

    return lagoon_size + len(trench.keys())


if __name__ == "__main__":
    main()
