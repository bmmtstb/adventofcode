import unittest
from copy import deepcopy
from functools import cache

from helper.file import read_lines_as_list


def load_data(fp: str) -> list[int]:
    """Load data from file as a list of integers."""
    return read_lines_as_list(fp, inst=int, split=" ")[0]


@cache
def apply_rules(stone: int) -> list[int]:
    """Apply the rules to a single stone, but make sure to cache the results."""
    # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    if stone == 0:
        return [1]
    # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
    # The left half of the digits are engraved on the new left stone,
    # and the right half of the digits are engraved on the new right stone.
    # (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
    str_num = str(stone)
    if len(str_num) % 2 == 0:
        return [int(str_num[: len(str_num) // 2]), int(str_num[len(str_num) // 2 :])]
    # If none of the other rules apply, the stone is replaced by a new stone;
    # the old stone's number multiplied by 2024 is engraved on the new stone.
    return [stone * 2024]


@cache
def calculate_num_stones(stone: int, n: int) -> int:
    """Blink once and modify the stones accordingly."""
    if n == 0:
        return 1

    transformed_stones = apply_rules(stone)
    return sum(calculate_num_stones(num, n - 1) for num in transformed_stones)


def part1(stones: list[int], n: int = 25) -> int:
    """Part1: Modify the stones according to the blinking rules then return the length."""
    total_stones = 0
    for stone in stones:
        total_stones += calculate_num_stones(stone, n=n)
    return total_stones


class Test2024Day11(unittest.TestCase):

    fp = "./data/11-test.txt"
    test_data = load_data(fp)

    def test_part1(self):
        for n, length in [
            (1, 3),
            (5, 13),
            (6, 22),
            (25, 55312),
        ]:
            with self.subTest(msg="n: {}, length: {}".format(n, length)):
                self.assertEqual(part1(deepcopy(self.test_data), n=n), length)


if __name__ == "__main__":
    print(">>> Start Main 11:")
    puzzle_data = load_data("./data/11.txt")
    print("Part 1): ", part1(puzzle_data))
    print("Part 2): ", part1(puzzle_data, n=75))
    print("End Main 11<<<")
