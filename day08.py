from dataclasses import dataclass
from itertools import cycle
from sys import stdin
import re


RE_EDGE = re.compile(r"^(\w{3}) = \((\w{3}), (\w{3})\)$")

EdgeDict = dict[str, tuple[str, str]]


def main() -> None:
    map: Map = Map.from_string(stdin.read())
    print("Part 1:", steps_between(map, start="AAA", stop="ZZZ"))


@dataclass
class Map:
    instructions: list[int]
    edges: EdgeDict

    @staticmethod
    def from_string(data: str) -> "Map":
        def parse_line(line: str) -> tuple[str, tuple[str, str]]:
            m = RE_EDGE.match(line)
            assert m
            return (m.group(1), (m.group(2), m.group(3)))

        instructiondata, edgedata = data.split("\n\n")
        return Map(
            instructions=list(map(lambda x: 0 if x == "L" else 1, instructiondata)),
            edges=dict(parse_line(line) for line in edgedata.split("\n") if line),
        )


def steps_between(map: Map, start: str, stop: str) -> int:
    for count, instruction in enumerate(cycle(map.instructions), start=1):
        start = map.edges[start][instruction]
        if start == stop:
            return count
    assert None, "Unreachable"


if __name__ == "__main__":
    main()
