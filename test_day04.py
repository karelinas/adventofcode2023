import unittest

from day04 import parse_cards, total_score, Card, count_scratch_cards


class Day04TestCase(unittest.TestCase):
    def test_example_data(self):
        example_data = (
            "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\n"
            "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\n"
            "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\n"
            "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\n"
            "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\n"
            "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11\n"
        )
        cards: list[Card] = parse_cards(example_data)
        with self.subTest(msg="Part 1"):
            self.assertEqual(total_score(cards), 13)
        with self.subTest(msg="Part 2"):
            self.assertEqual(count_scratch_cards(cards), 30)

    def test_real_data(self):
        with open("inputs/day04.txt", "r") as f:
            data = f.read()
            cards: list[Card] = parse_cards(data)
            with self.subTest(msg="Part 1"):
                self.assertEqual(total_score(cards), 23235)
            with self.subTest(msg="Part 2"):
                self.assertEqual(count_scratch_cards(cards), 5920640)
