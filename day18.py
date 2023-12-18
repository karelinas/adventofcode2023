import re
from dataclasses import dataclass
from sys import stdin

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


def make_polygon(trench: list[DigInstruction]) -> list[Point]:
    points: list[Point] = [Point(0, 0)]

    for instr in trench:
        points.append(points[-1] + instr.direction * instr.distance)

    return points


def determinant(p1: Point, p2: Point) -> int:
    # |x1 x2| = x1*y2 - x2*y1
    # |y1 y2|
    return p1.x * p2.y - p2.x * p1.y


def lagoon_size(instructions: list[DigInstruction]) -> int:
    vertices = make_polygon(instructions)

    # shoelace formula: https://en.wikipedia.org/wiki/Shoelace_formula
    inner_area: float = (
        sum(
            determinant(p1, p2)
            for p1, p2 in zip(vertices, vertices[1:] + [vertices[0]])
        )
        // 2
    )

    # pick's theorem: https://en.wikipedia.org/wiki/Pick%27s_theorem
    edge_points = sum(instr.distance for instr in instructions)
    area: int = int(inner_area + edge_points // 2 + 1)

    return area


if __name__ == "__main__":
    main()
