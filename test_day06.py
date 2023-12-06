import unittest

from day06 import parse_races, parse_races_bad_kerning, total_winning_strategies


class Day06TestCase(unittest.TestCase):
    def test_example_data(self):
        example_data = "Time:      7  15   30\n" "Distance:  9  40  200\n"

        with self.subTest(msg="Part 1"):
            races = parse_races(example_data)
            self.assertEqual(total_winning_strategies(races), 288)
        with self.subTest(msg="Part 1"):
            races = parse_races_bad_kerning(example_data)
            self.assertEqual(total_winning_strategies(races), 71503)

    @unittest.skip("slow unoptimized solution")
    def test_real_data(self):
        with open("inputs/day06.txt", "r") as f:
            data = f.read()
            with self.subTest(msg="Part 1"):
                races = parse_races(data)
                self.assertEqual(total_winning_strategies(races), 449550)
            with self.subTest(msg="Part 1"):
                races = parse_races_bad_kerning(data)
                self.assertEqual(total_winning_strategies(races), 28360140)
