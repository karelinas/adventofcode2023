import unittest

from day16 import Beam, Grid, count_energized_tiles, most_energized_configuration
from lib import Point


class Day16TestCase(unittest.TestCase):
    def test_example_data(self):
        # Have to escape left mirror '\' so this is ugly. Tried r-strings and
        # multi-line strings but none worked great with backslashes. Oh well.
        example_data = (
            ".|...\\....\n"
            "|.-.\\.....\n"
            ".....|-...\n"
            "........|.\n"
            "..........\n"
            ".........\\\n"
            "..../.\\\\..\n"
            ".-.-/..|..\n"
            ".|....-|.\\\n"
            "..//.|....\n"
        )
        grid = Grid.from_string(example_data)

        with self.subTest(msg="Part 1"):
            start_beam = Beam(pos=Point(-1, 0), v=Point(1, 0))
            self.assertEqual(count_energized_tiles(grid, start_beam), 46)

        with self.subTest(msg="Part 2"):
            self.assertEqual(most_energized_configuration(grid), 51)

    @unittest.skip("Too slow; takes 10 seconds")
    def test_real_data(self):
        with open("inputs/day16.txt", "r") as f:
            data = f.read()
            grid = Grid.from_string(data)

            with self.subTest(msg="Part 1"):
                start_beam = Beam(pos=Point(-1, 0), v=Point(1, 0))
                self.assertEqual(count_energized_tiles(grid, start_beam), 7111)

            with self.subTest(msg="Part 2"):
                self.assertEqual(most_energized_configuration(grid), 7831)
