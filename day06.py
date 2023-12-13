import re
from dataclasses import dataclass
from math import ceil, floor, prod, sqrt
from sys import stdin

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
    # Travel time:
    #
    #   t = r - b            (1)
    #
    # Where: t = travel time
    #        r = race time
    #        b = button press duration
    #
    # Travel distance:
    #
    #   s = b * t            (2)
    #
    # Where: s = distance traveled (set to race.record + 1)
    #
    # Substitute (1) in (2):
    #
    #   s = b*(r - b)
    #   s = b*r - b**2
    #   b**2 - r*b + s = 0   (3)
    #
    # Solve (3) for b using the quadratic equation:
    #
    #   b1 = (-r - sqrt(r**2 - 4 * s)) / 2
    #   b2 = (-r + sqrt(r**2 - 4 * s)) / 2
    #
    # Where b1 is the minimum button press duration to win the race, and b2 is the
    # maximum button press duration to win the race.
    #
    # The number of button press durations that win is the number of integers
    # between b1 and b2

    r = race.max_time
    s = race.record + 1

    b1: float = (-r - sqrt(r**2 - 4 * s)) / 2
    b2: float = (-r + sqrt(r**2 - 4 * s)) / 2

    return floor(b2) - ceil(b1) + 1


def total_winning_strategies(races: list[Race]) -> int:
    return prod(count_winning_strategies(r) for r in races)


if __name__ == "__main__":
    main()
