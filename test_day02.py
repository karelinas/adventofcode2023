import unittest

from day02 import CubeCounts, games_from_string, power_sum, sum_of_possible_games


class Day02TestCase(unittest.TestCase):
    def test_example_data(self):
        example_data = (
            "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n"
            "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\n"
            "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\n"
            "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\n"
            "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green\n"
        )
        games = games_from_string(example_data)
        bag = CubeCounts(red_count=12, green_count=13, blue_count=14)
        with self.subTest(msg="Part 1"):
            self.assertEqual(sum_of_possible_games(games, bag), 8)
        with self.subTest(msg="Part 2"):
            self.assertEqual(power_sum(games), 2286)

    def test_real_data(self):
        with open("inputs/day02.txt", "r") as f:
            games = games_from_string(f.read())
            bag = CubeCounts(red_count=12, green_count=13, blue_count=14)
            with self.subTest(msg="Part 1"):
                self.assertEqual(sum_of_possible_games(games, bag), 2156)
            with self.subTest(msg="Part 2"):
                self.assertEqual(power_sum(games), 66909)
