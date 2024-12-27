import unittest
from functools import cache

from helper.file import load_file_and_split


Towels = tuple[str]
Patterns = list[str]


def load_data(fp: str) -> tuple[Towels, Patterns]:
    """load the towels and patterns from the file"""
    towels, patterns = load_file_and_split(fp, "\n\n")
    return tuple(towels.split(", ")), patterns.split("\n")


@cache
def is_design_possible(towels: Towels, pattern: str) -> bool:
    """Check if a design is possible."""
    if len(pattern) == 0:
        return True
    for towel in towels:
        if pattern.startswith(towel) and is_design_possible(towels=towels, pattern=pattern[len(towel) :]):
            return True
    return False


@cache
def get_nof_possible_designs(towels: Towels, pattern: str) -> int:
    """Get the number of possible towel arrangements for each pattern."""
    if len(pattern) == 0:
        return 1

    total = 0

    for towel in towels:
        if pattern.startswith(towel) and is_design_possible(towels=towels, pattern=pattern[len(towel) :]):
            total += get_nof_possible_designs(towels=towels, pattern=pattern[len(towel) :])
    return total


def part1(towels: Towels, patterns: Patterns) -> int:
    """Part1: Get the number of possible designs."""
    return sum(is_design_possible(towels=towels, pattern=pattern) for pattern in patterns)


def part2(towels: Towels, patterns: Patterns) -> int:
    """Part2: Get the total number of possible ways to arrange each design."""
    return sum(get_nof_possible_designs(towels=towels, pattern=pattern) for pattern in patterns)


class Test2024Day19(unittest.TestCase):

    fp = "./data/19-test.txt"
    test_data = load_data(fp)

    def test_p1(self):
        self.assertEqual(part1(*self.test_data), 6)

    def test_p2(self):
        self.assertEqual(part2(*self.test_data), 16)

    def test_is_design_possible(self):
        for i, possible in enumerate(
            [
                True,
                True,
                True,
                True,
                False,
                True,
                True,
                False,
            ]
        ):
            with self.subTest(msg="i: {}, possible: {}".format(i, possible)):
                self.assertEqual(..., ...)


if __name__ == "__main__":
    print(">>> Start Main 19:")
    puzzle_data = load_data("./data/19.txt")
    print("Part 1): ", part1(*puzzle_data))
    print("Part 2): ", part2(*puzzle_data))
    print("End Main 19<<<")
