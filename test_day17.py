import unittest

from day17 import Grid, min_heat_loss
from lib import Point


class Day17TestCase(unittest.TestCase):
    def test_example_data(self):
        example_data = (
            "2413432311323\n"
            "3215453535623\n"
            "3255245654254\n"
            "3446585845452\n"
            "4546657867536\n"
            "1438598798454\n"
            "4457876987766\n"
            "3637877979653\n"
            "4654967986887\n"
            "4564679986453\n"
            "1224686865563\n"
            "2546548887735\n"
            "4322674655533\n"
        )
        grid = Grid.from_string(example_data)

        with self.subTest(msg="Part 1"):
            got = min_heat_loss(grid, Point(0, 0), Point(grid.max_x, grid.max_y))
            self.assertEqual(got, 102)

        with self.subTest(msg="Part 2"):
            got = min_heat_loss(
                grid,
                Point(0, 0),
                Point(grid.max_x, grid.max_y),
                min_streak=4,
                max_streak=10,
            )
            self.assertEqual(got, 94)

    @unittest.skip("Too slow; takes 10 seconds")
    def test_real_data(self):
        with open("inputs/day17.txt", "r") as f:
            data = f.read()
            grid = Grid.from_string(data)

            with self.subTest(msg="Part 1"):
                got = min_heat_loss(grid, Point(0, 0), Point(grid.max_x, grid.max_y))
                self.assertEqual(got, 843)

            with self.subTest(msg="Part 2"):
                got = min_heat_loss(
                    grid,
                    Point(0, 0),
                    Point(grid.max_x, grid.max_y),
                    min_streak=4,
                    max_streak=10,
                )
                self.assertEqual(got, 1017)
