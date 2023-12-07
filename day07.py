from collections import Counter
from dataclasses import dataclass
from typing import Sequence
from enum import IntEnum, auto
from sys import stdin


def main() -> None:
    data: str = stdin.read()
    hands: list[Hand] = parse_hands(data)
    print("Part 1", winnings(hands))
    joker_hands: list[HandWithJokers] = parse_hands_with_jokers(data)
    print("Part 2", winnings(joker_hands))


class HandType(IntEnum):
    HighCard: int = auto()
    OnePair: int = auto()
    TwoPair: int = auto()
    ThreeOfAKind: int = auto()
    FullHouse: int = auto()
    FourOfAKind: int = auto()
    FiveOfAKind: int = auto()


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
        type_counts: int = len(counts.values())

        if type_counts == 1:
            return HandType.FiveOfAKind
        elif type_counts == 2:
            # four of a kind
            if 4 in counts.values():
                return HandType.FourOfAKind
            else:
                return HandType.FullHouse
        elif type_counts == 3:
            if 3 in counts.values():
                return HandType.ThreeOfAKind
            else:
                return HandType.TwoPair
        elif type_counts == 4:
            return HandType.OnePair
        elif type_counts == 5:
            return HandType.HighCard

        assert None, "Never reached"

    def __lt__(self, rhs: "Hand") -> bool:
        t1: HandType = self.type
        t2: HandType = rhs.type

        # Better hand always wins
        if t1 != t2:
            return t1 < t2

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
        type_counts: int = len(counts.values())
        joker_count: int = counts.get("J") if "J" in counts else 0  # type: ignore

        if joker_count == 0:
            # no jokers, fall back to regular comparison
            return super().type

        if type_counts == 1 or type_counts == 2:
            return HandType.FiveOfAKind
        elif type_counts == 3:
            # four of a kind
            if any(joker_count + c == 4 for t, c in counts.items() if t != "J"):
                return HandType.FourOfAKind
            else:
                return HandType.FullHouse
        elif type_counts == 4:
            if any(joker_count + c == 3 for t, c in counts.items() if t != "J"):
                return HandType.ThreeOfAKind
            else:
                return HandType.TwoPair
        elif type_counts == 5:
            return HandType.OnePair

        assert None, "Never reached"

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
