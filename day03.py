from dataclasses import dataclass
from typing import Iterable
from sys import stdin
from collections import defaultdict
from math import prod


def main() -> None:
    schematic = Schematic.from_string(stdin.read())
    print("Part 1", sum_of_part_numbers(schematic))
    print("Part 2", sum_of_gear_ratios(schematic))


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, rhs: "Point") -> "Point":
        return Point(x=self.x + rhs.x, y=self.y + rhs.y)


class GridDict(dict[Point, str]):
    def __missing__(self, key: Point) -> str:
        return "."


@dataclass
class Part:
    numbers: list[int]
    symbol: str


@dataclass
class Schematic:
    parts: list[Part]

    @staticmethod
    def from_string(data: str) -> "Schematic":
        grid = GridDict(
            (Point(x, y), ch)
            for y, line in enumerate(data.split("\n"))
            for x, ch in enumerate(line.strip())
            if line and ch != "."
        )

        return Schematic(
            parts=[
                Part(numbers=list(nearby_numbers(grid, p)), symbol=symbol)
                for p, symbol in find_symbols(grid)
            ]
        )


def find_symbols(grid: GridDict) -> Iterable[tuple[Point, str]]:
    return (
        (p, symbol)
        for p, symbol in grid.items()
        if symbol != "." and not symbol.isdigit()
    )


def nearby_numbers(grid: GridDict, p: Point) -> Iterable[int]:
    used: set[Point] = set()
    deltas: list[Point] = [
        Point(-1, -1),
        Point(0, -1),
        Point(1, -1),
        Point(-1, 0),
        Point(1, 0),
        Point(-1, 1),
        Point(0, 1),
        Point(1, 1),
    ]
    neighborhood: list[Point] = [p + d for d in deltas]
    for q in neighborhood:
        if q in used or not grid[q].isdigit():
            continue

        # find beginning of number
        while grid[q + Point(-1, 0)].isdigit():
            q = q + Point(-1, 0)

        # collect all digits of the number
        digits: list[str] = []
        while grid[q].isdigit():
            digits.append(grid[q])
            used.add(q)
            q = q + Point(1, 0)

        # turn the number to int
        yield int("".join(digits))


def sum_of_part_numbers(schematic: Schematic) -> int:
    return sum(sum(p.numbers) for p in schematic.parts)


def sum_of_gear_ratios(schematic: Schematic) -> int:
    return sum(prod(part.numbers) for part in schematic.parts if len(part.numbers) == 2)


if __name__ == "__main__":
    main()
