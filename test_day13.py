import unittest

from day13 import apparent_reflection_summary, parse_grids, real_reflection_summary


class Day13TestCase(unittest.TestCase):
    def test_example_data(self):
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
        with self.subTest(msg="Part 1"):
            self.assertEqual(apparent_reflection_summary(grids), 405)
        with self.subTest(msg="Part 2"):
            self.assertEqual(real_reflection_summary(grids), 400)

    def test_real_data(self):
        with open("inputs/day13.txt", "r") as f:
            data = f.read()
            grids = parse_grids(data)
            with self.subTest(msg="Part 1"):
                self.assertEqual(apparent_reflection_summary(grids), 34772)
            with self.subTest(msg="Part 2"):
                self.assertEqual(real_reflection_summary(grids), 35554)
