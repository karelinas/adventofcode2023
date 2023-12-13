from collections import Counter
from dataclasses import dataclass
from enum import IntEnum
from sys import stdin
from typing import Sequence


def main() -> None:
    data: str = stdin.read()
    hands: list[Hand] = parse_hands(data)
    print("Part 1", winnings(hands))
    joker_hands: list[HandWithJokers] = parse_hands_with_jokers(data)
    print("Part 2", winnings(joker_hands))


class HandType(IntEnum):
    HighCard: int = 11111
    OnePair: int = 1112
    TwoPair: int = 122
    ThreeOfAKind: int = 113
    FullHouse: int = 23
    FourOfAKind: int = 14
    FiveOfAKind: int = 5


@dataclass(eq=True, frozen=True)
class Card:
    label: str

    @property
    def value(self):
        if self.label == "A":
            return 14
        elif self.label == "K":
            return 13
        elif self.label == "Q":
            return 12
        elif self.label == "J":
            return 11
        elif self.label == "T":
            return 10
        else:
            return int(self.label)


@dataclass(eq=True, frozen=True)
class MaybeJoker(Card):
    @property
    def value(self):
        if self.label == "J":
            return 1
        return super().value


@dataclass
class Hand:
    cards: list[Card]
    bid: int

    @property
    def type(self) -> HandType:
        counts = Counter(c.label for c in self.cards)
        return self._type_from_counts(list(counts.values()))

    @staticmethod
    def _type_from_counts(counts: list[int]) -> HandType:
        type_number: int = sum(
            v * 10**n for n, v in enumerate(reversed(sorted(counts)))
        )
        return HandType(type_number)

    def __lt__(self, rhs: "Hand") -> bool:
        t1: HandType = self.type
        t2: HandType = rhs.type

        # Better hand always wins
        if t1 != t2:
            return t1 > t2

        # Equal hand is ranked by better card in earlier position
        for c1, c2 in zip(self.cards, rhs.cards):
            if c1 != c2:
                return c1.value < c2.value

        assert None, "Never reached"

    @staticmethod
    def from_string(data: str) -> "Hand":
        carddata, biddata = data.split(" ")
        return Hand(cards=[Card(label=label) for label in carddata], bid=int(biddata))


@dataclass
class HandWithJokers(Hand):
    @property
    def type(self) -> HandType:
        """best possible hand taking jokers into account"""
        counts = Counter(c.label for c in self.cards)

        joker_count: int = counts.get("J") if "J" in counts else 0  # type: ignore

        if joker_count != 0 and joker_count != 5:
            # take the jokers out
            del counts["J"]
            # put the jokers back in as the best card
            most_common_label = counts.most_common(1)[0][0]
            counts[most_common_label] += joker_count

        return self._type_from_counts(list(counts.values()))

    @staticmethod
    def from_string(data: str) -> "HandWithJokers":
        carddata, biddata = data.split(" ")
        return HandWithJokers(
            cards=[MaybeJoker(label=label) for label in carddata], bid=int(biddata)
        )


def parse_hands(data: str) -> list[Hand]:
    return [Hand.from_string(line.strip()) for line in data.split("\n") if line]


def parse_hands_with_jokers(data: str) -> list[HandWithJokers]:
    return [
        HandWithJokers.from_string(line.strip()) for line in data.split("\n") if line
    ]


def winnings(hands: Sequence[Hand]) -> int:
    return sum(rank * hand.bid for rank, hand in enumerate(sorted(hands), start=1))


if __name__ == "__main__":
    main()
