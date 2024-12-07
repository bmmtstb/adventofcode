import unittest

from helper.file import load_file_and_split
from helper.tuple import tuple_add_tuple, tuple_mult_scalar


WORD: str = "XMAS"


def load_data(fp: str) -> list[str]:
    """Load the data from the file. Make sure to exclude the last (empty) line."""
    d = load_file_and_split(fp, sep="\n")
    if d[-1] == "":
        return d[:-1]
    return d


def contains_xmas(grid: list[str], r_i, c_i) -> int:
    """Check whether the word XMAS starts at the given position."""
    nof_rows, nof_cols = len(grid), len(grid[0])
    assert all(len(row) == nof_cols for row in grid)

    total = 0

    for direction in [
        # up
        (-1, -1),
        (-1, 0),
        (-1, 1),
        # horizontal
        (0, -1),
        (0, 1),
        # down
        (1, -1),
        (1, 0),
        (1, 1),
    ]:
        curr_pos: tuple[int, int] = (r_i, c_i)
        # skip early if the final position is out of bounds
        final_r, final_c = tuple_add_tuple(curr_pos, tuple_mult_scalar(direction, 3))
        if final_r < 0 or final_r >= nof_rows or final_c < 0 or final_c >= nof_cols:
            continue

        for char in WORD:
            if grid[curr_pos[0]][curr_pos[1]] != char:
                break
            curr_pos = tuple_add_tuple(curr_pos, direction)
        else:
            total += 1
            continue
    return total


def contains_crossed_mas(grid: list[str], r_i, c_i) -> bool:
    """Check whether the current position is the middle point of two crossed "MAS"."""
    assert grid[r_i][c_i] == "A"

    # unnecessary because we iterate and skip the border
    # rows, cols = len(grid), len(grid[0])
    # if r_i - 1 < 0 or r_i + 1 >= rows or c_i - 1 < 0 or c_i + 1 >= cols:
    #     return False

    if (grid[r_i - 1][c_i - 1] + grid[r_i + 1][c_i + 1] in ["MS", "SM"]) and (
        (grid[r_i - 1][c_i + 1] + grid[r_i + 1][c_i - 1] in ["MS", "SM"])
    ):
        return True

    return False


def part1(grid: list[str]) -> int:
    """Part1: Find all occurrences of the word XMAS in the grid."""
    total = 0
    for r_i, row in enumerate(grid):
        for c_i, char in enumerate(row):
            if char == "X":
                total += contains_xmas(grid, r_i, c_i)
    return total


def part2(grid: list[str]) -> int:
    """Part2: Find all occurrences where two "MAS" cross each other."""
    total = 0
    for r_i, row in enumerate(grid[1:-1], start=1):
        for c_i, char in enumerate(row[1:-1], start=1):
            if char == "A":
                total += int(contains_crossed_mas(grid, r_i, c_i))
    return total


class Test2024Day04(unittest.TestCase):

    fp = "./data/04-test.txt"
    data = load_data(fp)

    def test_p1(self):
        self.assertEqual(part1(self.data), 18)

    def test_p2(self):
        self.assertEqual(part2(self.data), 9)

    def test_p2_puzzle(self):
        self.assertEqual(part2(load_data("./data/04.txt")), 1948)


if __name__ == "__main__":
    print(">>> Start Main 04:")
    data = load_data("./data/04.txt")
    print("Part 1): ", part1(data))
    print("Part 2): ", part2(data))  # 1948
    print("End Main 04<<<")
