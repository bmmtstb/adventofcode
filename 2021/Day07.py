import unittest
from typing import Dict, List, Tuple, Set

from helper.file import load_file_and_split


def get_fuel_efficient_level(pos: List[int], steps: str = "lin") -> int:
    """Given the crabs positions, calculate the most fuel-efficient level to move them to"""
    # set best to highest val possible
    best = len(pos) * sum(i for i in range(0, max(pos) + 1, 1))
    a = min(pos)
    while a <= max(pos):
        if steps == "lin":
            curr = sum(abs(val - a) for val in pos)
        elif steps == "exp":
            curr = sum(sum(range(0, abs(val - a) + 1, 1)) for val in pos)
        else:
            raise Exception("Invalid step-function")

        if curr >= best:  # only one minimum -> if value goes up minimum was already found
            return best
        else:
            best = curr
            a += 1
    raise Exception("no optima found")


class Test2021Day07(unittest.TestCase):
    def test_find_optima(self):
        for l, opt, step in [
            [[16, 1, 2, 0, 4, 2, 7, 1, 2, 14], 37, "lin"],
            [[16, 1, 2, 0, 4, 2, 7, 1, 2, 14], 168, "exp"],
            [[1, 2, 3], 2, "lin"],
            [[1, 2, 3], 2, "exp"],
            [list(range(1, 12, 1)), 30, "lin"],
            [list(range(1, 6, 1)), 6, "lin"],
            [list(range(1, 6, 1)), 8, "exp"],
        ]:
            with self.subTest():
                self.assertEqual(get_fuel_efficient_level(l, step), opt)


if __name__ == '__main__':
    print(">>> Start Main 07:")
    puzzle_input = load_file_and_split("data/07.txt", separator=",", instance_type=int)
    print("Part 1): ", get_fuel_efficient_level(puzzle_input.copy(), "lin"))
    print("Part 2): ", get_fuel_efficient_level(puzzle_input.copy(), "exp"))
    print("End Main 07<<<")
