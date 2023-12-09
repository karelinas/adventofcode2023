from sys import stdin
import re


RE_NUMBER = re.compile(r"-?\d+")

History = list[int]


def main() -> None:
    histories: list[History] = parse_histories(stdin.read())
    print("Part 1:", sum_of_next_values(histories))
    print("Part 2:", sum_of_previous_values(histories))


def parse_histories(data: str) -> list[History]:
    def parse_history(data: str) -> History:
        return [int(m) for m in RE_NUMBER.findall(data)]

    return [parse_history(line) for line in data.split("\n") if line]


def extrapolate_next_item(history: History) -> int:
    if all(n == 0 for n in history):
        return 0

    return history[-1] + extrapolate_next_item(
        [n2 - n1 for n1, n2 in zip(history, history[1:])]
    )


def sum_of_next_values(histories: list[History]) -> int:
    return sum(extrapolate_next_item(h) for h in histories)


def sum_of_previous_values(histories: list[History]) -> int:
    return sum(extrapolate_next_item(h[::-1]) for h in histories)


if __name__ == "__main__":
    main()
