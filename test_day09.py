import unittest

from day09 import parse_histories, sum_of_next_values, sum_of_previous_values


class Day09TestCase(unittest.TestCase):
    def test_example_data(self):
        example_data = "0 3 6 9 12 15\n1 3 6 10 15 21\n10 13 16 21 30 45\n"
        histories = parse_histories(example_data)

        with self.subTest(msg="Part 1"):
            self.assertEqual(sum_of_next_values(histories), 114)
        with self.subTest(msg="Part 2"):
            self.assertEqual(sum_of_previous_values(histories), 2)

    def test_real_data(self):
        with open("inputs/day09.txt", "r") as f:
            data = f.read()
            histories = parse_histories(data)
            with self.subTest(msg="Part 1"):
                self.assertEqual(sum_of_next_values(histories), 1757008019)
            with self.subTest(msg="Part 2"):
                self.assertEqual(sum_of_previous_values(histories), 995)
