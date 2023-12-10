import unittest

from day10 import Grid, loop_length, count_enclosed_tiles


class Day10TestCase(unittest.TestCase):
    def test_example_data_part1(self):
        example_data = "..F7.\n.FJ|.\nSJ.L7\n|F--J\nLJ...\n"
        grid = Grid.from_string(example_data)
        self.assertEqual(loop_length(grid), 16)

    def test_example_data_part2(self):
        example_data = (
            "FF7FSF7F7F7F7F7F---7\n"
            "L|LJ||||||||||||F--J\n"
            "FL-7LJLJ||||||LJL-77\n"
            "F--JF--7||LJLJ7F7FJ-\n"
            "L---JF-JLJ.||-FJLJJ7\n"
            "|F|F-JF---7F7-L7L|7|\n"
            "|FFJF7L7F-JF7|JL---7\n"
            "7-L-JL7||F7|L7F-7F7|\n"
            "L.L7LFJ|||||FJL7||LJ\n"
            "L7JLJL-JLJLJL--JLJ.L\n"
        )
        grid = Grid.from_string(example_data)
        self.assertEqual(count_enclosed_tiles(grid), 10)

    def test_real_data(self):
        with open("inputs/day10.txt", "r") as f:
            data = f.read()
            grid = Grid.from_string(data)
            with self.subTest(msg="Part 1"):
                self.assertEqual(loop_length(grid) // 2, 6951)
            with self.subTest(msg="Part 2"):
                self.assertEqual(count_enclosed_tiles(grid), 563)
