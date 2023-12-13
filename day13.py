from lib import transpose
from dataclasses import dataclass
from enum import IntEnum
from typing import Iterable
from sys import stdin


def main() -> None:
    grids = parse_grids(stdin.read())
    print("Part 1:", reflection_summary(grids))


@dataclass
class Grid:
    rows: list[int]
    columns: list[int]

    @staticmethod
    def from_string(data: str) -> "Grid":
        lines = data.split("\n")
        return Grid(
            rows=[hash(line) for line in lines],
            columns=[hash("".join(column)) for column in transpose(lines)],
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
    def neighboring_identical_lines(lines: list[int]) -> Iterable[int]:
        for idx, (a, b) in enumerate(zip(lines, lines[1:])):
            if a == b:
                yield idx

    def is_mirror_point(lines: list[int], idx: int) -> bool:
        return all(a == b for a, b in zip(reversed(lines[: idx + 1]), lines[idx + 1 :]))

    for maybe_reflection in neighboring_identical_lines(grid.rows):
        if is_mirror_point(grid.rows, maybe_reflection):
            return ReflectionPoint(
                reflection_type=ReflectionType.Horizontal,
                lines_before=maybe_reflection + 1,
            )

    for maybe_reflection in neighboring_identical_lines(grid.columns):
        if is_mirror_point(grid.columns, maybe_reflection):
            return ReflectionPoint(
                reflection_type=ReflectionType.Vertical,
                lines_before=maybe_reflection + 1,
            )

    assert None, "No reflection points found"


def reflection_summary(grids: list[Grid]) -> int:
    return sum(find_reflection(g).reflection_value for g in grids)


if __name__ == "__main__":
    main()
