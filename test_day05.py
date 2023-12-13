import unittest

from day05 import Almanac, lowest_location


class Day05TestCase(unittest.TestCase):
    def test_example_data(self):
        example_data = (
            "seeds: 79 14 55 13\n"
            "\n"
            "seed-to-soil map:\n"
            "50 98 2\n"
            "52 50 48\n"
            "\n"
            "soil-to-fertilizer map:\n"
            "0 15 37\n"
            "37 52 2\n"
            "39 0 15\n"
            "\n"
            "fertilizer-to-water map:\n"
            "49 53 8\n"
            "0 11 42\n"
            "42 0 7\n"
            "57 7 4\n"
            "\n"
            "water-to-light map:\n"
            "88 18 7\n"
            "18 25 70\n"
            "\n"
            "light-to-temperature map:\n"
            "45 77 23\n"
            "81 45 19\n"
            "68 64 13\n"
            "\n"
            "temperature-to-humidity map:\n"
            "0 69 1\n"
            "1 0 69\n"
            "\n"
            "humidity-to-location map:\n"
            "60 56 37\n"
            "56 93 4\n"
        )
        with self.subTest(msg="Part 1"):
            almanac = Almanac.from_string(example_data)
            self.assertEqual(lowest_location(almanac), 35)
        with self.subTest(msg="Part 2"):
            almanac = Almanac.from_string(example_data, seeds_as_ranges=True)
            self.assertEqual(lowest_location(almanac), 46)

    def test_real_data(self):
        with open("inputs/day05.txt", "r") as f:
            data = f.read()
            with self.subTest(msg="Part 1"):
                almanac = Almanac.from_string(data)
                self.assertEqual(lowest_location(almanac), 510109797)
            with self.subTest(msg="Part 2"):
                almanac = Almanac.from_string(data, seeds_as_ranges=True)
                self.assertEqual(lowest_location(almanac), 9622622)
