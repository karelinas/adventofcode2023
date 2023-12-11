import unittest

from day11 import GridDict, sum_of_distances, expand_universe


class Day11TestCase(unittest.TestCase):
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
        grid = GridDict.from_string(example_data)

        with self.subTest(msg="Part 1"):
            grid_part1 = expand_universe(grid)
            self.assertEqual(sum_of_distances(grid_part1), 374)
        with self.subTest(msg="Part 2", hubble_constant=10):
            grid_part2_10 = expand_universe(grid, hubble_constant=10)
            self.assertEqual(sum_of_distances(grid_part2_10), 1030)
        with self.subTest(msg="Part 2", hubble_constant=100):
            grid_part2_100 = expand_universe(grid, hubble_constant=100)
            self.assertEqual(sum_of_distances(grid_part2_100), 8410)

    def test_real_data(self):
        with open("inputs/day11.txt", "r") as f:
            data = f.read()
            grid = GridDict.from_string(data)
            with self.subTest(msg="Part 1"):
                grid_part1 = expand_universe(grid)
                self.assertEqual(sum_of_distances(grid_part1), 9609130)
            with self.subTest(msg="Part 2"):
                grid_part2 = expand_universe(grid, hubble_constant=1000000)
                self.assertEqual(sum_of_distances(grid_part2), 702152204842)
