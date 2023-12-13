import unittest

from day12 import (
    SpringRow,
    count_arrangements,
    parse_spring_rows,
    unfold_row,
    unfold_rows,
)


class Day12TestCase(unittest.TestCase):
    def test_example_data_part1(self):
        test_data: list[tuple[str, int]] = [
            ("???.### 1,1,3", 1),
            (".??..??...?##. 1,1,3", 4),
            ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
            ("????.#...#... 4,1,1", 1),
            ("????.######..#####. 1,6,5", 4),
            ("?###???????? 3,2,1", 10),
        ]
        for data, expected in test_data:
            with self.subTest(data=data, expected=expected):
                row = SpringRow.from_string(data)
                self.assertEqual(count_arrangements(row), expected)

    def test_example_data_part2(self):
        test_data: list[tuple[str, int]] = [
            ("???.### 1,1,3", 1),
            (".??..??...?##. 1,1,3", 16384),
            ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
            ("????.#...#... 4,1,1", 16),
            ("????.######..#####. 1,6,5", 2500),
            ("?###???????? 3,2,1", 506250),
        ]
        for data, expected in test_data:
            with self.subTest(data=data, expected=expected):
                row = unfold_row(SpringRow.from_string(data))
                self.assertEqual(count_arrangements(row), expected)

    @unittest.skip("Too slow; takes 20 seconds")
    def test_real_data(self):
        with open("inputs/day12.txt", "r") as f:
            data = f.read()
            rows = parse_spring_rows(data)
            with self.subTest(msg="Part 1"):
                total = sum(count_arrangements(row) for row in rows)
                self.assertEqual(total, 7195)
            with self.subTest(msg="Part 2"):
                rows = unfold_rows(rows)
                total = sum(count_arrangements(row) for row in rows)
                self.assertEqual(total, 33992866292225)
