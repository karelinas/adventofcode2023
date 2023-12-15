import unittest

from day15 import sum_of_hashes


class Day15TestCase(unittest.TestCase):
    def test_example_data(self):
        example_data = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
        with self.subTest(msg="Part 1"):
            self.assertEqual(sum_of_hashes(example_data), 1320)
