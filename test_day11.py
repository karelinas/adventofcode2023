import unittest

from day11 import parse_grid, sum_of_distances, expand_universe


class Day10TestCase(unittest.TestCase):
    def test_example_data_part1(self):
        example_data = (
            "...#......\n"
            ".......#..\n"
            "#.........\n"
            "..........\n"
            "......#...\n"
            ".#........\n"
            ".........#\n"
            "..........\n"
            ".......#..\n"
            "#...#.....\n"
        )
        grid = parse_grid(example_data)
        grid = expand_universe(grid)
        self.assertEqual(sum_of_distances(grid), 374)
