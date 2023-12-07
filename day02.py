from collections import defaultdict
from dataclasses import dataclass
from sys import stdin
from typing import Optional
import re

RE_GAME = re.compile(r"Game (\d+): (.*)")
RE_CUBE = re.compile(r"(\d+) (red|green|blue)")


def main() -> None:
    games: list[GameRecord] = games_from_string(stdin.read())
    bag = CubeCounts(red_count=12, green_count=13, blue_count=14)
    print("Part 1:", sum_of_possible_games(games, bag))
    print("Part 2:", power_sum(games))


@dataclass(frozen=True)
class CubeCounts:
    red_count: int = 0
    green_count: int = 0
    blue_count: int = 0

    def power(self) -> int:
        return self.red_count * self.green_count * self.blue_count

    @staticmethod
    def from_string(data: str) -> "CubeCounts":
        matches: list[Optional[re.Match[str]]] = [
            RE_CUBE.match(cubestr) for cubestr in data.split(", ")
        ]
        counts: dict[str, int] = defaultdict(
            int, {m.group(2): int(m.group(1)) for m in matches if m is not None}
        )
        return CubeCounts(
            red_count=counts["red"],
            green_count=counts["green"],
            blue_count=counts["blue"],
        )


@dataclass(frozen=True)
class GameRecord:
    game_id: int
    counts: list[CubeCounts]

    def power(self) -> int:
        max_counts = CubeCounts(
            red_count=max(self.counts, key=lambda c: c.red_count).red_count,
            green_count=max(self.counts, key=lambda c: c.green_count).green_count,
            blue_count=max(self.counts, key=lambda c: c.blue_count).blue_count,
        )
        return max_counts.power()

    def is_possible(self, bag: CubeCounts) -> bool:
        return all(
            c.red_count <= bag.red_count
            and c.green_count <= bag.green_count
            and c.blue_count <= bag.blue_count
            for c in self.counts
        )

    @staticmethod
    def from_string(data: str) -> "GameRecord":
        mo = RE_GAME.match(data)
        assert mo is not None
        return GameRecord(
            game_id=int(mo.group(1)),
            counts=[
                CubeCounts.from_string(handful) for handful in mo.group(2).split("; ")
            ],
        )


def games_from_string(data: str) -> list[GameRecord]:
    return [GameRecord.from_string(line.strip()) for line in data.split("\n") if line]


def sum_of_possible_games(games: list[GameRecord], bag: CubeCounts) -> int:
    return sum(game.game_id if game.is_possible(bag) else 0 for game in games)


def power_sum(games: list[GameRecord]) -> int:
    return sum(game.power() for game in games)


if __name__ == "__main__":
    main()
