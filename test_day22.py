import unittest

from day22 import (
    count_safe_to_disintegrate,
    parse_bricks,
    simulate_gravity,
    sum_of_best_chain_reactions,
)


class Day22TestCase(unittest.TestCase):
    def test_example_data(self):
        example_data = (
            "1,0,1~1,2,1\n"
            "0,0,2~2,0,2\n"
            "0,2,3~2,2,3\n"
            "0,0,4~0,2,4\n"
            "2,0,5~2,2,5\n"
            "0,1,6~2,1,6\n"
            "1,1,8~1,1,9\n"
        )
        bricks = parse_bricks(example_data)
        fallen_bricks = simulate_gravity(bricks)

        with self.subTest(msg="Part 1"):
            self.assertEqual(count_safe_to_disintegrate(fallen_bricks), 5)

        with self.subTest(msg="Part 2"):
            self.assertEqual(sum_of_best_chain_reactions(fallen_bricks), 7)

    @unittest.skip("Too slow; takes 1 second")
    def test_real_data(self):
        with open("inputs/day22.txt", "r") as f:
            data = f.read()
            bricks = parse_bricks(data)
            fallen_bricks = simulate_gravity(bricks)

            with self.subTest(msg="Part 1"):
                self.assertEqual(count_safe_to_disintegrate(fallen_bricks), 495)

            with self.subTest(msg="Part 2"):
                self.assertEqual(sum_of_best_chain_reactions(fallen_bricks), 76158)
