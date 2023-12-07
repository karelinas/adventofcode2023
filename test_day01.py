import unittest

from day01 import CalibrationDocument, CorrectedCalibrationDocument


class Day01TestCase(unittest.TestCase):
    def test_calibration_value_example_part1(self):
        example_input = "1abc2\npqr3stu8vwx\na1b2c3d4e5f\ntreb7uchet\n"
        document = CalibrationDocument.from_string(example_input)
        self.assertEqual(document.calibration_value(), 142)

    def test_calibration_value_example_part2(self):
        example_input = (
            "two1nine\n"
            "eightwothree\n"
            "abcone2threexyz\n"
            "xtwone3four\n"
            "4nineeightseven2\n"
            "zoneight234\n"
            "7pqrstsixteen\n"
        )
        document = CorrectedCalibrationDocument.from_string(example_input)
        self.assertEqual(document.calibration_value(), 281)

    def test_overlapping_digit_names(self):
        document = CorrectedCalibrationDocument.from_string("2eighthree")
        self.assertEqual(document.calibration_value(), 23)

    def test_real_input(self):
        with open("inputs/day01.txt", "r") as f:
            data: str = f.read()
            document = CalibrationDocument.from_string(data)
            correct_document = CorrectedCalibrationDocument.from_string(data)
            with self.subTest(msg="Part 1"):
                self.assertEqual(document.calibration_value(), 55123)
            with self.subTest(msg="Part 2"):
                self.assertEqual(correct_document.calibration_value(), 55260)
