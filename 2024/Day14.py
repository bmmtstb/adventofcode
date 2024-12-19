import re
import unittest

from helper.file import read_lines_as_list
from helper.tuple import tuple_add_tuple, tuple_mod_tuple

Position = tuple[int, int]


def load_data(fp: str) -> list[tuple[Position, Position]]:
    """Read all the positions and velocities from a file."""
    lines = read_lines_as_list(fp)
    robots = []
    for line in lines:
        p1, p2, v1, v2 = re.findall(r"-*\d+", line)
        robots.append(
            (
                (int(p1), int(p2)),
                (int(v1), int(v2)),
            )
        )
    return robots


def move_robot(pos: Position, vel: Position, n: int, width: int, height: int) -> Position:
    """Given the initial position and velocity, move the robot n times."""
    curr = pos
    shape = (width, height)
    for _ in range(n):
        curr = tuple_mod_tuple(tuple_add_tuple(curr, vel), shape)
    return curr


def print_robots(positions: list[Position], shape: Position) -> None:
    """Given the current positions of the robots, show them on a map."""
    for i in range(shape[1]):
        print(
            "".join(
                str(sum((i, j) == pos for pos in positions)) if (i, j) in positions else "." for j in range(shape[0])
            )
        )


def part1(robots: list[tuple[Position, Position]], height: int = 103, width: int = 101) -> int:
    """Part1: Compute the safety factor after moving the robots for 100 time steps."""
    time: int = 100

    ul, ur, ll, lr = 0, 0, 0, 0

    half_width = int(width / 2)
    half_height = int(height / 2)

    final_positions: list[Position] = []

    for robot in robots:
        final_positions.append(move_robot(*robot, n=time, width=width, height=height))

    # print_robots(final_positions, shape=(width, height))

    for final_pos in final_positions:
        if final_pos[0] < half_width and final_pos[1] < half_height:
            ul += 1
        elif final_pos[0] >= half_width + 1 and final_pos[1] < half_height:
            ur += 1
        elif final_pos[0] < half_width and final_pos[1] >= half_height + 1:
            ll += 1
        elif final_pos[0] >= half_width + 1 and final_pos[1] >= half_height + 1:
            lr += 1

    return ul * ur * ll * lr


def part2() -> ...:
    """Part2: ..."""


class Test2024Day14(unittest.TestCase):

    fp = "./data/14-test.txt"
    test_data = load_data(fp)
    test_height: int = 7
    test_width: int = 11

    def test_p1(self):
        self.assertEqual(part1(self.test_data, height=self.test_height, width=self.test_width), 12)

    def test_robot_positions(self):
        start_pos = (2, 4)
        vel = (2, -3)
        for i, pos in enumerate(
            [
                (4, 1),
                (6, 5),
                (8, 2),
                (10, 6),
                (1, 3),
            ],
            start=1,
        ):
            with self.subTest(msg=f"steps: {i}"):
                self.assertEqual(
                    move_robot(pos=start_pos, vel=vel, height=self.test_height, width=self.test_width, n=i), pos
                )


if __name__ == "__main__":
    print(">>> Start Main 14:")
    puzzle_data = load_data("./data/14.txt")
    print("Part 1): ", part1(puzzle_data))
    print("Part 2): ", part2())
    print("End Main 14<<<")
