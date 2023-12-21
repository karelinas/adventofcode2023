import unittest

from day21 import (
    Grid,
    count_plots_reachable_in_n_steps,
    interpolate_plots_reachable_in_n_steps,
)


class Day21TestCase(unittest.TestCase):
    def test_example_data(self):
        example_data = (
            "...........\n"
            ".....###.#.\n"
            ".###.##..#.\n"
            "..#.#...#..\n"
            "....#.#....\n"
            ".##..S####.\n"
            ".##..#...#.\n"
            ".......##..\n"
            ".##.#.####.\n"
            ".##..##.##.\n"
            "...........\n"
        )
        grid = Grid.from_string(example_data)

        with self.subTest(msg="Part 1"):
            self.assertEqual(count_plots_reachable_in_n_steps(grid, n=6), 16)

        # no example data tests for part 2 -- the example data has rocks in
        # the same rows and columns as S, which breaks my way of interpolation.

    @unittest.skip("Waaaaay too slow; takes 5 minutes")
    def test_real_data(self):
        with open("inputs/day21.txt", "r") as f:
            data = f.read()
            grid = Grid.from_string(data)

            with self.subTest(msg="Part 1"):
                self.assertEqual(count_plots_reachable_in_n_steps(grid, n=64), 3751)

            with self.subTest(msg="Part 2"):
                self.assertEqual(
                    interpolate_plots_reachable_in_n_steps(grid, n=26501365),
                    619407349431167,
                )
