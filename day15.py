from functools import reduce
from sys import stdin
from typing import Callable


def main() -> None:
    data: str = stdin.read()
    print("Part 1:", sum_of_hashes(data))


def reindeer_hash(data: str) -> int:
    hash_fn: Callable[[int, str], int] = lambda res, ch: ((res + ord(ch)) * 17) % 256
    return reduce(hash_fn, data, 0)


def sum_of_hashes(data: str) -> int:
    return sum(reindeer_hash(piece.strip()) for piece in data.split(","))


if __name__ == "__main__":
    main()
