import unittest
from typing import Dict, List, Tuple, Set

from helper.file import read_lines_as_list

Range = Tuple[int, int]
RangePair = Tuple[Range, Range]


def load_ranges(filepath: str) -> List[RangePair]:
    """load list from file, get list of two Ranges"""
    return [(
        tuple(map(int, range_pair[0].split("-"))),
        tuple(map(int, range_pair[1].split("-")))
    ) for range_pair in read_lines_as_list(filepath=filepath, split=",")]


def does_range_fully_contain_range(range_pair: RangePair) -> bool:
    """return whether r1 does fully contain r2 or vice versa"""
    r1, r2 = range_pair
    return (r1[0] >= r2[0] and r1[1] <= r2[1]) or (r2[0] >= r1[0] and r2[1] <= r1[1])


def does_range_overlap(range_pair: RangePair) -> bool:
    """return whether r1 does overlap with r2"""
    r1, r2 = range_pair
    return r2[0] <= r1[0] <= r2[1] or r2[0] <= r1[1] <= r2[1] or r1[0] <= r2[0] <= r1[1] or r1[0] <= r2[1] <= r1[1]


def count_fully_containing(ranges: List[RangePair]) -> int:
    """count all range pairs where one fully contains the other"""
    return sum(does_range_fully_contain_range(range_pair) for range_pair in ranges)


def count_overlapping(ranges: List[RangePair]) -> int:
    """count all range pairs where one fully contains the other"""
    return sum(does_range_overlap(range_pair) for range_pair in ranges)


class Test2022Day04(unittest.TestCase):
    test_data = load_ranges("data/04-test.txt")

    def test_does_range_fully_contain_range(self):
        for i, contains in [
            (0, False),
            (1, False),
            (2, False),
            (3, True),
            (4, True),
            (5, True),
            (6, False),
            (7, False),
            (8, False),
        ]:
            with self.subTest(msg=f'Pair {i}: {self.test_data[i]}'):
                self.assertEqual(does_range_fully_contain_range(self.test_data[i]), contains)

    def test_count_fully_containing(self):
        self.assertEqual(count_fully_containing(self.test_data), 3)

    def test_does_range_overlap(self):
        for i, contains in [
            (0, False),
            (1, False),
            (2, True),
            (3, True),
            (4, True),
            (5, True),
            (6, True),
            (7, True),
            (8, False),
        ]:
            with self.subTest(msg=f'Pair {i}: {self.test_data[i]}'):
                self.assertEqual(does_range_overlap(self.test_data[i]), contains)

    def test_count_overlapping(self):
        self.assertEqual(count_overlapping(self.test_data), 6)


if __name__ == '__main__':
    print(">>> Start Main 04:")
    puzzle_input = load_ranges("data/04.txt")
    print("Part 1): ", count_fully_containing(puzzle_input))
    print("Part 2): ", count_overlapping(puzzle_input))
    print("End Main 04<<<")