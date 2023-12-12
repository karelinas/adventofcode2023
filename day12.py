from enum import IntEnum, auto
from dataclasses import dataclass
from sys import stdin
from functools import cache


def main() -> None:
    rows = parse_spring_rows(stdin.read())
    print("Part 1:", sum(count_arrangements(row) for row in rows))
    rows = unfold_rows(rows)
    print("Part 2:", sum(count_arrangements(row) for row in rows))


class SpringStatus(IntEnum):
    Operational: int = auto()
    Damaged: int = auto()
    Unknown: int = auto()

    @staticmethod
    def from_string(data: str) -> "SpringStatus":
        if data == ".":
            return SpringStatus.Operational
        elif data == "#":
            return SpringStatus.Damaged
        elif data == "?":
            return SpringStatus.Unknown

        assert None, f"Invalid spring status: '{data}'"

    def __repr__(self) -> str:
        return "".join(
            "."
            if self == SpringStatus.Operational
            else "#"
            if self == SpringStatus.Damaged
            else "?"
        )


@dataclass(eq=True, frozen=True)
class SpringRow:
    springs: tuple[SpringStatus, ...]
    damaged_groups: tuple[int, ...]

    @staticmethod
    def from_string(data: str) -> "SpringRow":
        rowdata, damagedata = data.split(" ")
        return SpringRow(
            springs=tuple(SpringStatus.from_string(ch) for ch in rowdata),
            damaged_groups=tuple(int(s) for s in damagedata.split(",")),
        )


def parse_spring_rows(data: str) -> list[SpringRow]:
    return [SpringRow.from_string(line) for line in data.split("\n") if line]


@cache
def count_arrangements(row: SpringRow, current_group=0) -> int:
    if len(row.springs) == 0:
        groups = list(row.damaged_groups)
        if current_group != 0:
            if not groups or current_group != groups.pop(0):
                return 0
        return 0 if groups else 1

    spring = row.springs[0]
    if spring == SpringStatus.Operational:
        new_groups = row.damaged_groups
        if current_group > 0:
            if not row.damaged_groups or row.damaged_groups[0] != current_group:
                return 0
            new_groups = new_groups[1:]
        return count_arrangements(
            SpringRow(springs=row.springs[1:], damaged_groups=new_groups)
        )
    elif spring == SpringStatus.Damaged:
        return count_arrangements(
            SpringRow(springs=row.springs[1:], damaged_groups=row.damaged_groups),
            current_group=current_group + 1,
        )
    else:
        operational = SpringRow(
            springs=(SpringStatus.Operational,) + row.springs[1:],
            damaged_groups=row.damaged_groups,
        )
        damaged = SpringRow(
            springs=(SpringStatus.Damaged,) + row.springs[1:],
            damaged_groups=row.damaged_groups,
        )
        return count_arrangements(operational, current_group) + count_arrangements(
            damaged, current_group
        )


def unfold_row(row: SpringRow) -> SpringRow:
    new_springs = ((row.springs + (SpringStatus.Unknown,)) * 5)[:-1]
    return SpringRow(
        springs=new_springs,
        damaged_groups=row.damaged_groups * 5,
    )


def unfold_rows(rows: list[SpringRow]) -> list[SpringRow]:
    return [unfold_row(row) for row in rows]


if __name__ == "__main__":
    main()
