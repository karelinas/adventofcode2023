import unittest

from day15 import parse_steps, sum_of_hashes, total_focusing_power


class Day15TestCase(unittest.TestCase):
    def test_example_data(self):
        steps = parse_steps("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7")
        with self.subTest(msg="Part 1"):
            self.assertEqual(sum_of_hashes(steps), 1320)
        with self.subTest(msg="Part 2"):
            self.assertEqual(total_focusing_power(steps), 145)

    def test_real_data(self):
        with open("inputs/day15.txt", "r") as f:
            data = f.read()
            steps = parse_steps(data)
            with self.subTest(msg="Part 1"):
                self.assertEqual(sum_of_hashes(steps), 498538)
            with self.subTest(msg="Part 2"):
                self.assertEqual(total_focusing_power(steps), 286278)
