import re
from collections import defaultdict, namedtuple
from dataclasses import dataclass, field
from operator import attrgetter
from sys import stdin
from typing import Iterable

RE_BRICK = re.compile(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)")


def main() -> None:
    bricks = parse_bricks(stdin.read())
    fallen_bricks = simulate_gravity(bricks)
    print("Part 1:", count_safe_to_disintegrate(fallen_bricks))
    print("Part 2:", sum_of_best_chain_reactions(fallen_bricks))


Point3D = namedtuple("Point3D", ["x", "y", "z"])


def translate_point3d(point: Point3D, delta: Point3D) -> Point3D:
    return Point3D(point.x + delta.x, point.y + delta.y, point.z + delta.z)


@dataclass(eq=True, frozen=True)
class Brick:
    start: Point3D
    end: Point3D
    label: int = 0
    supported_by: set[int] = field(default_factory=set)

    @staticmethod
    def from_string(data: str) -> "Brick":
        mo = RE_BRICK.match(data)
        assert mo
        x1, y1, z1, x2, y2, z2 = list(map(int, mo.groups()))
        return Brick(
            start=Point3D(min(x1, x2), min(y1, y2), min(z1, z2)),
            end=Point3D(max(x1, x2), max(y1, y2), max(z1, z2)),
        )

    def with_label(self, label: int) -> "Brick":
        return Brick(
            start=self.start, end=self.end, label=label, supported_by=self.supported_by
        )

    def with_supported_by(self, supported_by: set[int]) -> "Brick":
        return Brick(
            start=self.start, end=self.end, label=self.label, supported_by=supported_by
        )

    def translated(self, delta: Point3D) -> "Brick":
        return Brick(
            start=translate_point3d(self.start, delta),
            end=translate_point3d(self.end, delta),
            label=self.label,
            supported_by=self.supported_by,
        )

    @property
    def lowest_z(self) -> int:
        return min(self.start.z, self.end.z)

    def each_cube(self) -> Iterable[Point3D]:
        for x in range(self.start.x, self.end.x + 1):
            for y in range(self.start.y, self.end.y + 1):
                for z in range(self.start.z, self.end.z + 1):
                    yield Point3D(x, y, z)


def parse_bricks(data: str) -> list[Brick]:
    return [
        Brick.from_string(line).with_label(label)
        for label, line in enumerate(data.split("\n"))
        if line
    ]


def simulate_gravity(bricks: Iterable[Brick]) -> list[Brick]:
    def drop_brick(grid3d: dict[Point3D, int], brick: Brick) -> Brick:
        z = brick.lowest_z

        if z == 1:
            return brick

        supporting_z: int = 0
        for p in brick.each_cube():
            if p.z != z:
                continue
            cubes_below = [k for k in grid3d.keys() if k.x == p.x and k.y == p.y]
            if not cubes_below:
                continue
            supporting_z = max(supporting_z, max(c.z for c in cubes_below))
        return brick.translated(Point3D(0, 0, supporting_z - z + 1))

    dropped_bricks: list[Brick] = []
    grid3d: dict[Point3D, int] = {}
    for brick in sorted(bricks, key=attrgetter("lowest_z")):
        brick = drop_brick(grid3d, brick)

        # fill in cubes and determine supports
        supports: set[int] = set()
        for p in brick.each_cube():
            grid3d[p] = brick.label
            if p.z != brick.lowest_z:
                continue
            below = translate_point3d(p, Point3D(0, 0, -1))
            if below in grid3d:
                supports.add(grid3d[below])
        dropped_bricks.append(brick.with_supported_by(supports))

    return dropped_bricks


def count_safe_to_disintegrate(bricks: list[Brick]) -> int:
    supports: dict[int, list[int]] = defaultdict(list)
    for brick in bricks:
        for supported_by in brick.supported_by:
            supports[supported_by].append(brick.label)

    bricks_by_label = {brick.label: brick for brick in bricks}

    disintegrate_count: int = 0
    for brick in bricks:
        if all(
            len(bricks_by_label[s].supported_by) >= 2 for s in supports[brick.label]
        ):
            disintegrate_count += 1

    return disintegrate_count


def sum_of_best_chain_reactions(bricks: list[Brick]) -> int:
    supports: dict[int, list[int]] = defaultdict(list)
    for brick in bricks:
        for supported_by in brick.supported_by:
            supports[supported_by].append(brick.label)

    bricks_by_label = {brick.label: brick for brick in bricks}

    chain_reaction_count: int = 0
    for brick in bricks:
        fallen: set[int] = set([brick.label])
        queue: list[int] = [brick.label]
        while queue:
            q = queue.pop(0)
            for s in supports[q]:
                if s in fallen:
                    # don't disintegrate the same brick twice
                    continue
                if bricks_by_label[s].supported_by.issubset(fallen):
                    queue.append(s)
                    fallen.add(s)
                    chain_reaction_count += 1

    return chain_reaction_count


if __name__ == "__main__":
    main()
