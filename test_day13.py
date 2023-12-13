import unittest

from day13 import parse_grids, reflection_summary


class Day13TestCase(unittest.TestCase):
    def test_example_data_part1(self):
        example_data = (
            "#.##..##.\n"
            "..#.##.#.\n"
            "##......#\n"
            "##......#\n"
            "..#.##.#.\n"
            "..##..##.\n"
            "#.#.##.#.\n"
            "\n"
            "#...##..#\n"
            "#....#..#\n"
            "..##..###\n"
            "#####.##.\n"
            "#####.##.\n"
            "..##..###\n"
            "#....#..#\n"
        )
        grids = parse_grids(example_data)
        self.assertEqual(reflection_summary(grids), 405)

    def test_real_data(self):
        with open("inputs/day13.txt", "r") as f:
            data = f.read()
            grids = parse_grids(data)
            with self.subTest(msg="Part 1"):
                self.assertEqual(reflection_summary(grids), 34772)
