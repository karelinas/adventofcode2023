import unittest

from day08 import Map, steps_between, ghost_steps


class Day08TestCase(unittest.TestCase):
    def test_example_data_part1(self):
        example_data = "LLR\n\nAAA = (BBB, BBB)\nBBB = (AAA, ZZZ)\nZZZ = (ZZZ, ZZZ)\n"

        map = Map.from_string(example_data)
        self.assertEqual(steps_between(map, start="AAA", stop="ZZZ"), 6)

    def test_example_data_part2(self):
        example_data = (
            "LR\n"
            "\n"
            "11A = (11B, XXX)\n"
            "11B = (XXX, 11Z)\n"
            "11Z = (11B, XXX)\n"
            "22A = (22B, XXX)\n"
            "22B = (22C, 22C)\n"
            "22C = (22Z, 22Z)\n"
            "22Z = (22B, 22B)\n"
            "XXX = (XXX, XXX)\n"
        )

        map = Map.from_string(example_data)
        self.assertEqual(ghost_steps(map), 6)

    def test_real_data(self):
        with open("inputs/day08.txt", "r") as f:
            data = f.read()
            map = Map.from_string(data)
            with self.subTest(msg="Part 1"):
                self.assertEqual(steps_between(map, start="AAA", stop="ZZZ"), 19783)
            with self.subTest(msg="Part 2"):
                self.assertEqual(ghost_steps(map), 9177460370549)
