import unittest
import re

from helper.file import load_file_and_split


def load_data(fp: str) -> str:
    """Part1: Load the corrupted data as a long string."""
    return "\n".join(load_file_and_split(fp))


def part1(corrupted_data: str) -> int:
    """Part1: Compute the sum of all multiplications in the corrupted data."""
    occurrences = re.findall(
        pattern=r"mul\((\d{1,3}),(\d{1,3})\)", string=corrupted_data
    )
    return sum(int(a) * int(b) for a, b in occurrences)


def part2(corrupted_data: str) -> int:
    """Part2: Compute the sum of multiplication but keep track of do and don'ts."""
    occurrences = re.findall(
        pattern=r"(do)\(\)|(don't)\(\)|mul\((\d{1,3}),(\d{1,3})\)",
        string=corrupted_data,
    )
    enabled = True
    total = 0
    for occurrence in occurrences:
        if occurrence[0] == "do":
            enabled = True
        elif occurrence[1] == "don't":
            enabled = False
        else:
            if enabled:
                _, _, a, b = occurrence
                total += int(a) * int(b)
    return total


class Test2024Day03(unittest.TestCase):

    fp = "./data/03-test.txt"
    data = load_data(fp)

    def test_load_data(self):
        self.assertTrue(isinstance(self.data, str))
        self.assertTrue(self.data.startswith("xmul"))

    def test_p1(self):
        for data, r in [
            (self.data, 161),
            ("mul(1,2)mul(3,4)mul(5,6)!", 44),
            ("mul(1,2)\nmul(1,2)", 4),
        ]:
            with self.subTest(msg="data: {}, r: {}".format(data, r)):
                self.assertEqual(part1(data), r)

    def test_p2(self):
        self.assertEqual(part2(self.data), 48)


if __name__ == "__main__":
    print(">>> Start Main 03:")
    PUZZLE = load_data("./data/03.txt")
    print("Part 1): ", part1(PUZZLE))
    print("Part 2): ", part2(PUZZLE))
    print("End Main 03<<<")
