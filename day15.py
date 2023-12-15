from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from sys import stdin
from typing import Callable, Mapping, MutableMapping


def main() -> None:
    steps = parse_steps(stdin.read())
    print("Part 1:", sum_of_hashes(steps))
    print("Part 2:", total_focusing_power(steps))


def parse_steps(data: str) -> list[str]:
    return [piece.strip() for piece in data.split(",")]


def reindeer_hash(data: str) -> int:
    hash_fn: Callable[[int, str], int] = lambda res, ch: ((res + ord(ch)) * 17) % 256
    return reduce(hash_fn, data, 0)


def sum_of_hashes(steps: list[str]) -> int:
    return sum(reindeer_hash(s.strip()) for s in steps)


@dataclass
class Lens:
    label: str
    focal_length: int

    @staticmethod
    def from_string(data: str) -> "Lens":
        l, d = data.split("=")
        return Lens(label=l, focal_length=int(d))


def build_boxes(steps: list[str]) -> Mapping[int, list[Lens]]:
    boxes: MutableMapping[int, list[Lens]] = defaultdict(list[Lens])
    for s in steps:
        if "=" in s:
            # insert or replace lens
            new_lens = Lens.from_string(s)
            box_number = reindeer_hash(new_lens.label)

            if any(new_lens.label == lens.label for lens in boxes[box_number]):
                # replace existing lens
                boxes[box_number] = [
                    lens if new_lens.label != lens.label else new_lens
                    for lens in boxes[box_number]
                ]
            else:
                # insert new lens
                boxes[box_number].append(new_lens)

        elif "-" in s:
            # remove lens if it exists
            label, _ = s.split("-")
            box_number = reindeer_hash(label)
            boxes[box_number] = [
                lens for lens in boxes[box_number] if lens.label != label
            ]

        else:
            raise RuntimeError(f"Invalid step '{s}'")

    return boxes


def total_focusing_power(steps: list[str]) -> int:
    boxes = build_boxes(steps)
    return sum(
        (box_number + 1) * (slot_number) * lens.focal_length
        for box_number, lenses in boxes.items()
        for slot_number, lens in enumerate(lenses, start=1)
    )


if __name__ == "__main__":
    main()
