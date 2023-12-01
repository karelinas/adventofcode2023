import unittest

from day01 import calibration_value, corrected_calibration_value


class Day01TestCase(unittest.TestCase):
    def test_calibration_value_part1_example(self):
        example_input = "1abc2\npqr3stu8vwx\na1b2c3d4e5f\ntreb7uchet\n"
        self.assertEqual(calibration_value(example_input), 142)

    def test_calibration_value_part2_example(self):
        example_input = "two1nine\neightwothree\nabcone2threexyz\nxtwone3four\n4nineeightseven2\nzoneight234\n7pqrstsixteen\n"
        self.assertEqual(corrected_calibration_value(example_input), 281)

    def test_overlapping_digit_names(self):
        self.assertEqual(corrected_calibration_value("2eighthree"), 23)

    def test_real_input(self):
        with open("inputs/day01.txt", "r") as f:
            calibration_document: str = f.read()
            self.assertEqual(calibration_value(calibration_document), 55123)
            self.assertEqual(corrected_calibration_value(calibration_document), 55260)
