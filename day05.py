from dataclasses import dataclass
from typing import Iterable
from sys import stdin


def main() -> None:
    data = stdin.read()
    almanac = Almanac.from_string(data)
    print("Part 1:", lowest_location(almanac))
    almanac2 = Almanac.from_string(data, seeds_as_ranges=True)
    print("Part 2:", lowest_location(almanac2))


@dataclass(frozen=True, eq=True)
class CategoryRange:
    source: range
    target: range

    def offset(self) -> int:
        return self.target.start - self.source.start


@dataclass(frozen=True, eq=True, repr=True)
class CategoryMap:
    source: str
    target: str
    maps: list[CategoryRange]

    def map_range(self, r: range) -> list[range]:
        mapped: list[range] = []
        unmapped: list[range] = [r]
        for mp in self.maps:
            if not unmapped:
                break
            new_unmapped: list[range] = []
            while unmapped:
                u, m = self._map_range_helper(unmapped.pop(), mp)
                mapped.extend(m)
                new_unmapped.extend(u)
            unmapped = new_unmapped

        mapped.extend(unmapped)
        return mapped

    @staticmethod
    def _map_range_helper(
        r: range, c: CategoryRange
    ) -> tuple[list[range], list[range]]:
        """split range r into mapped and unmapped parts"""

        offset: int = c.offset()
        s: range = c.source
        unmapped: list[range] = []
        mapped: list[range] = []

        if r.start < s.start and r.stop > s.stop:
            # s is wholly contained within r
            #
            # r.start    s.start               s.stop     r.stop
            #    V          V                     V          V
            #    +----------+---------------------+----------+
            #    | unmapped |       mapped        | unmapped |
            #    +----------+---------------------+----------+
            unmapped = [
                range(r.start, s.start),
                range(s.stop, r.stop),
            ]
            mapped = [range(s.start + offset, s.stop + offset)]
        elif r.start >= s.start and r.stop <= s.stop:
            # r is wholly contained by or equal to s
            #
            # s.start    r.start               r.stop     s.stop
            #    V          V                     V          V
            #    +----------+---------------------+----------+
            #    |          |       mapped        |          |
            #    +----------+---------------------+----------+
            unmapped = []
            mapped = [range(r.start + offset, r.stop + offset)]
        elif r.start < s.start and r.stop > s.start:
            # r overlaps s from left
            #
            # r.start    s.start               r.stop     s.stop
            #    V          V                     V          V
            #    +----------+---------------------+----------+
            #    | unmapped |       mapped        |          |
            #    +----------+---------------------+----------+
            unmapped = [range(r.start, s.start)]
            mapped = [range(s.start + offset, r.stop + offset)]
        elif r.start < s.stop and r.stop > s.stop:
            # r overlaps s from right
            #
            # s.start    r.start               s.stop     r.stop
            #    V          V                     V          V
            #    +----------+---------------------+----------+
            #    |          |       mapped        | unmapped |
            #    +----------+---------------------+----------+
            unmapped = [range(s.stop, r.stop)]
            mapped = [range(r.start + offset, s.stop + offset)]
        else:
            # no overlap
            unmapped = [r]
            mapped = []

        return unmapped, mapped

    @staticmethod
    def from_string(data: str) -> "CategoryMap":
        header, *lines = data.split("\n")

        assert header.endswith(" map:")
        src, tgt = header[:-5].split("-to-")
        maps: list[CategoryRange] = []

        for line in lines:
            if not line:
                continue

            tgt_start, src_start, count = list(map(int, line.split(" ")))
            maps.append(
                CategoryRange(
                    source=range(src_start, src_start + count),
                    target=range(tgt_start, tgt_start + count),
                )
            )

        return CategoryMap(source=src, target=tgt, maps=maps)


@dataclass
class Almanac:
    seeds: list[range]
    maps: dict[str, CategoryMap]

    @staticmethod
    def from_string(data: str, seeds_as_ranges: bool = False) -> "Almanac":
        seed_data, *maps_data = data.split("\n\n")

        assert seed_data.startswith("seeds: ")
        seed_numbers: list[int] = list(map(int, seed_data[7:].split(" ")))
        seeds: list[range] = []
        if seeds_as_ranges:
            seeds = [
                range(s, s + c) for s, c in zip(seed_numbers[0::2], seed_numbers[1::2])
            ]
        else:
            seeds = [range(s, s + 1) for s in seed_numbers]

        maps: Iterable[CategoryMap] = (CategoryMap.from_string(m) for m in maps_data)

        return Almanac(seeds=seeds, maps={m.source: m for m in maps})


def traverse(almanac: Almanac, r: range, category: str = "seed") -> list[range]:
    if category not in almanac.maps:
        return [r]

    mapped_ranges: list[range] = almanac.maps[category].map_range(r)
    next_traversal: list[range] = []
    for m in mapped_ranges:
        next_traversal.extend(traverse(almanac, m, almanac.maps[category].target))
    return next_traversal


def lowest_location(almanac: Almanac) -> int:
    return min(min(r.start for r in traverse(almanac, seed)) for seed in almanac.seeds)


if __name__ == "__main__":
    main()
