from dataclasses import dataclass
from sys import stdin


def main():
    cards = parse_cards(stdin.read())
    print("Part 1:", total_score(cards))
    print("Part 2:", count_scratch_cards(cards))


@dataclass(frozen=True, eq=True)
class Card:
    got: set[int]
    winning: set[int]


def parse_cards(data: str) -> list[Card]:
    cards: list[Card] = []

    for line in data.split("\n"):
        if not line:
            continue
        _, rest = line.split(":", maxsplit=1)
        winning, got = rest.split("|", maxsplit=1)
        cards.append(
            Card(
                got=set(int(n.strip()) for n in got.split(" ") if n.strip()),
                winning=set(int(n.strip()) for n in winning.split(" ") if n.strip()),
            )
        )

    return cards


def total_score(cards: list[Card]) -> int:
    matches = (c.got & c.winning for c in cards)
    return sum(2 ** (len(m) - 1) for m in matches if m)


def count_scratch_cards(cards: list[Card]) -> int:
    counts: list[int] = [1 for _ in range(len(cards))]

    for card_number, c in enumerate(cards):
        match_count = len(c.got & c.winning)
        for i in range(card_number + 1, card_number + match_count + 1):
            counts[i] += counts[card_number]

    return sum(counts)


if __name__ == "__main__":
    main()
