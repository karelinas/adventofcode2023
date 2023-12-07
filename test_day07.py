import unittest

from day07 import parse_hands, parse_hands_with_jokers, winnings


class Day07TestCase(unittest.TestCase):
    def test_example_data(self):
        example_data = (
            "32T3K 765\n" "T55J5 684\n" "KK677 28\n" "KTJJT 220\n" "QQQJA 483\n"
        )

        with self.subTest(msg="Part 1"):
            hands = parse_hands(example_data)
            self.assertEqual(winnings(hands), 6440)
        with self.subTest(msg="Part 2"):
            hands = parse_hands_with_jokers(example_data)
            self.assertEqual(winnings(hands), 5905)

    def test_real_data(self):
        with open("inputs/day07.txt", "r") as f:
            data = f.read()
            with self.subTest(msg="Part 1"):
                hands = parse_hands(data)
                self.assertEqual(winnings(hands), 251216224)
            with self.subTest(msg="Part 2"):
                hands = parse_hands_with_jokers(data)
                self.assertEqual(winnings(hands), 250825971)
