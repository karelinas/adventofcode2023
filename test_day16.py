import unittest

from day16 import Beam, Grid, count_energized_tiles
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
        start_beam = Beam(pos=Point(-1, 0), v=Point(1, 0))
        self.assertEqual(count_energized_tiles(grid, start_beam), 46)
