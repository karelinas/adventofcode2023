from dataclasses import dataclass
from sys import stdin
from math import prod
import re


RE_NUMBER = re.compile(r"\d+")


@dataclass
class Race:
    max_time: int
    record: int


def main() -> None:
    data: str = stdin.read()
    races = parse_races(data)
    print("Part 1", total_winning_strategies(races))
    races = parse_races_bad_kerning(data)
    print("Part 2", total_winning_strategies(races))


def parse_races(data: str) -> list[Race]:
    timedata, distancedata, *_ = data.split("\n")
    return [
        Race(max_time=int(t), record=int(r))
        for t, r in zip(RE_NUMBER.findall(timedata), RE_NUMBER.findall(distancedata))
    ]


def parse_races_bad_kerning(data: str) -> list[Race]:
    def combine_int(intdata: list[str]) -> int:
        return int("".join(intdata))

    timedata, distancedata, *_ = data.split("\n")
    return [
        Race(
            max_time=combine_int(RE_NUMBER.findall(timedata)),
            record=combine_int(RE_NUMBER.findall(distancedata)),
        )
    ]


def distance_traveled(v: int, t: int) -> int:
    return v * t


def count_winning_strategies(race: Race) -> int:
    return sum(
        1
        for a in range(race.max_time)
        if distance_traveled(a, race.max_time - a) > race.record
    )


def total_winning_strategies(races: list[Race]) -> int:
    return prod(count_winning_strategies(r) for r in races)


if __name__ == "__main__":
    main()
