import unittest
from functools import cache

from helper.file import load_file_and_split

Position = tuple[int, int]

PRIZE_A = 3
PRIZE_B = 1
MAX_STEP = 100
OFFSET = 10_000_000_000_000


@cache
def solve_machine(a: Position, b: Position, prize: Position, tolerance: float = 1e-5, offset: int = 0) -> int | None:
    """Given the positions of the machines, calculate the minimal prize when playing this arcade."""

    a1, a2 = a
    b1, b2 = b
    p1, p2 = prize

    p1 += offset
    p2 += offset

    # p = m * a + n * b
    # => solve one line for n and substitute into the other line

    m = (b1 * p2 - p1 * b2) / (b1 * a2 - a1 * b2)
    n = (p1 - m * a1) / b1

    # assert m < MAX_STEP and n < MAX_STEP, f"m {m} or n {n} is too large."

    if abs(m - round(m)) < tolerance and abs(n - round(n)) < tolerance:
        return round(m) * PRIZE_A + round(n) * PRIZE_B

    return None


def load_data(fp: str) -> list[tuple[Position, Position, Position]]:
    """Get the configurations of the machines."""
    data = load_file_and_split(fp, sep="\n\n")

    machines = []

    for machine in data:
        a, b, prize = machine.split("\n")
        a: Position = tuple(map(int, [val[2:] for val in a.split(": ")[1].split(", ")]))
        b: Position = tuple(map(int, [val[2:] for val in b.split(": ")[1].split(", ")]))
        prize: Position = tuple(map(int, [val[2:] for val in prize.split(": ")[1].split(", ")]))

        machines.append((a, b, prize))

    return machines


def part1(data: list[tuple[Position, Position, Position]]) -> int:
    """Part1: Get the minimum number of tokens to spend."""
    total = 0
    for machine in data:
        res = solve_machine(*machine)
        if res is not None:
            total += res
    return total


def part2(data: list[tuple[Position, Position, Position]]) -> int:
    """Part2: Part 1 with offset"""
    total = 0
    for machine in data:
        res = solve_machine(*machine, offset=OFFSET)
        if res is not None:
            total += res
    return total


class Test2024Day13(unittest.TestCase):

    fp = "./data/13-test.txt"
    test_data = load_data(fp)

    def test_solve_machine(self):
        for i, cost in enumerate([280, None, 200, None]):
            with self.subTest(msg="i: {}, cost: {}".format(i, cost)):
                self.assertEqual(solve_machine(*self.test_data[i]), cost)

    def test_p1(self):
        self.assertEqual(part1(self.test_data), 480)

    def test_p2(self):
        self.assertEqual(part2(self.test_data), 875318608908)


if __name__ == "__main__":
    print(">>> Start Main 13:")
    puzzle_data = load_data("./data/13.txt")
    print("Part 1): ", part1(puzzle_data))
    print("Part 2): ", part2(puzzle_data))
    print("End Main 13<<<")
