from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush
from sys import stdin

from lib import Point, orthogonal_directions


def main() -> None:
    grid = Grid.from_string(stdin.read())
    print(
        "Part 1:",
        min_heat_loss(
            grid=grid, start=Point(0, 0), finish=Point(grid.max_x, grid.max_y)
        ),
    )
    print(
        "Part 1:",
        min_heat_loss(
            grid=grid,
            start=Point(0, 0),
            finish=Point(grid.max_x, grid.max_y),
            min_streak=4,
            max_streak=10,
        ),
    )


@dataclass
class Grid:
    grid: dict[Point, int]
    max_x: int
    max_y: int

    @staticmethod
    def from_string(data: str) -> "Grid":
        new_grid = {
            Point(x, y): int(ch)
            for y, line in enumerate(data.split("\n"))
            if line
            for x, ch in enumerate(line)
        }
        max_x = max(p.x for p in new_grid.keys())
        max_y = max(p.y for p in new_grid.keys())
        return Grid(grid=new_grid, max_x=max_x, max_y=max_y)


def min_heat_loss(
    grid: Grid, start: Point, finish: Point, min_streak: int = 1, max_streak: int = 3
) -> int:
    # cost, position, direction
    QueueItem = tuple[int, Point, Point]
    # coord, direction
    CostKey = tuple[Point, Point]

    queue: list[QueueItem] = []
    heappush(queue, (0, start, Point(0, 0)))

    path_costs: dict[CostKey, int] = defaultdict(lambda: 2**32)
    seen: set[CostKey] = set()

    while queue:
        cost, pos, blocked_direction = heappop(queue)

        if pos == finish:
            return int(cost)

        if (pos, blocked_direction) in seen:
            continue
        seen.add((pos, blocked_direction))

        for direction in orthogonal_directions():
            if (
                direction == blocked_direction
                or direction.reverse() == blocked_direction
            ):
                # don't move twice in the same direction
                continue

            accumulated_cost: int = 0
            for distance in range(1, max_streak + 1):
                next_pos = pos + direction * distance

                if next_pos not in grid.grid:
                    continue

                accumulated_cost += grid.grid[next_pos]

                if distance < min_streak:
                    continue

                cost_to_destination = cost + accumulated_cost
                if cost_to_destination >= path_costs[(next_pos, direction)]:
                    continue

                path_costs[(next_pos, direction)] = cost_to_destination
                heappush(queue, (cost_to_destination, next_pos, direction))

    assert None, "Path not found"


if __name__ == "__main__":
    main()
