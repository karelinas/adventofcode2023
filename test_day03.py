import unittest

from day03 import Schematic, sum_of_part_numbers, sum_of_gear_ratios


class Day03TestCase(unittest.TestCase):
    def test_example_data(self):
        example_data = (
            "467..114..\n"
            "...*......\n"
            "..35..633.\n"
            "......#...\n"
            "617*......\n"
            ".....+.58.\n"
            "..592.....\n"
            "......755.\n"
            "...$.*....\n"
            ".664.598..\n"
        )
        schematic = Schematic.from_string(example_data)
        with self.subTest(msg="Part 1"):
            self.assertEqual(sum_of_part_numbers(schematic), 4361)
        with self.subTest(msg="Part 2"):
            self.assertEqual(sum_of_gear_ratios(schematic), 467835)

    def test_real_data(self):
        with open("inputs/day03.txt", "r") as f:
            data = f.read()
            schematic = Schematic.from_string(data)
            with self.subTest(msg="Part 1"):
                self.assertEqual(sum_of_part_numbers(schematic), 539713)
            with self.subTest(msg="Part 2"):
                self.assertEqual(sum_of_gear_ratios(schematic), 84159075)
