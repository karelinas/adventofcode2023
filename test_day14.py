import unittest

from day14 import Grid


class Day14TestCase(unittest.TestCase):
    def test_example_data(self):
        example_data = (
            "O....#....\n"
            "O.OO#....#\n"
            ".....##...\n"
            "OO.#O....O\n"
            ".O.....O#.\n"
            "O.#..O.#.#\n"
            "..O..#O..O\n"
            ".......O..\n"
            "#....###..\n"
            "#OO..#....\n"
        )
        grid = Grid.from_string(example_data)
        with self.subTest(msg="Part 1"):
            self.assertEqual(grid.tilt().load, 136)
        with self.subTest(msg="Part 2"):
            self.assertEqual(grid.n_cycles(1000000000).load, 64)

    @unittest.skip("Too slow; takes 10 seconds")
    def test_real_data(self):
        with open("inputs/day14.txt", "r") as f:
            data = f.read()
            grid = Grid.from_string(data)
            with self.subTest(msg="Part 1"):
                self.assertEqual(grid.tilt().load, 108889)
            with self.subTest(msg="Part 2"):
                self.assertEqual(grid.n_cycles(1000000000).load, 104671)
