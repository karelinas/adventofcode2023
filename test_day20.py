import unittest

from day20 import Machinery, fewest_pushes_for_rx_low


class Day20TestCase(unittest.TestCase):
    def test_example_data_1(self):
        example_data = (
            "broadcaster -> a, b, c\n"
            "%a -> b\n"
            "%b -> c\n"
            "%c -> inv\n"
            "&inv -> a\n"
        )
        machinery = Machinery.from_string(example_data)
        machinery.button_mash(1000)
        self.assertEqual(machinery.pulse_score(), 32000000)

    def test_example_data_2(self):
        example_data = (
            "broadcaster -> a\n"
            "%a -> inv, con\n"
            "&inv -> b\n"
            "%b -> con\n"
            "&con -> output\n"
        )
        machinery = Machinery.from_string(example_data)
        machinery.button_mash(1000)
        self.assertEqual(machinery.pulse_score(), 11687500)

    def test_real_data(self):
        with open("inputs/day20.txt", "r") as f:
            data = f.read()
            machinery = Machinery.from_string(data)

            with self.subTest(msg="Part 1"):
                machinery.button_mash(1000)
                self.assertEqual(machinery.pulse_score(), 800830848)

            with self.subTest(msg="Part 2"):
                self.assertEqual(fewest_pushes_for_rx_low(machinery), 244055946148853)
