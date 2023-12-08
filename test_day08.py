import unittest

from day08 import Map, steps_between


class Day07TestCase(unittest.TestCase):
    def test_example_data(self):
        example_data = "LLR\n\nAAA = (BBB, BBB)\nBBB = (AAA, ZZZ)\nZZZ = (ZZZ, ZZZ)\n"

        with self.subTest(msg="Part 1"):
            map = Map.from_string(example_data)
            self.assertEqual(steps_between(map, start="AAA", stop="ZZZ"), 6)
