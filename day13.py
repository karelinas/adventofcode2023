from dataclasses import dataclass
from enum import IntEnum
from functools import reduce
from operator import or_
from sys import stdin

from lib import transpose


def main() -> None:
    grids = parse_grids(stdin.read())
    print("Part 1:", reflection_summary(grids))


@dataclass
class Grid:
    rows: list[int]
    columns: list[int]

    @staticmethod
    def from_string(data: str) -> "Grid":
        def line_to_bits(line: str) -> int:
            return reduce(
                or_, (1 << shift if ch == "#" else 0 for shift, ch in enumerate(line))
            )

        lines = data.split("\n")
        return Grid(
            rows=[line_to_bits(line) for line in lines],
            columns=[line_to_bits("".join(column)) for column in transpose(lines)],
        )


class ReflectionType(IntEnum):
    Vertical = 1
    Horizontal = 100


@dataclass
class ReflectionPoint:
    reflection_type: ReflectionType
    lines_before: int

    @property
    def reflection_value(self) -> int:
        return self.reflection_type * self.lines_before


def parse_grids(data: str) -> list[Grid]:
    return [Grid.from_string(grid.strip()) for grid in data.split("\n\n") if grid]


def find_reflection(grid: Grid) -> ReflectionPoint:
    def is_mirror_point(lines: list[int], idx: int) -> bool:
        return all(a == b for a, b in zip(reversed(lines[: idx + 1]), lines[idx + 1 :]))

    for idx in range(len(grid.rows) - 1):
        if is_mirror_point(grid.rows, idx):
            return ReflectionPoint(
                reflection_type=ReflectionType.Horizontal,
                lines_before=idx + 1,
            )

    for idx in range(len(grid.columns) - 1):
        if is_mirror_point(grid.columns, idx):
            return ReflectionPoint(
                reflection_type=ReflectionType.Vertical,
                lines_before=idx + 1,
            )

    assert None, "No reflection points found"


def reflection_summary(grids: list[Grid]) -> int:
    return sum(find_reflection(g).reflection_value for g in grids)


if __name__ == "__main__":
    main()
