import unittest

from helper.file import read_lines_as_list
from helper.tuple import tuple_add_tuple

Position = tuple[int, int]
Positions = set[Position]

directions: Positions = {(-1, 0), (1, 0), (0, -1), (0, 1)}


def load_data(fp: str) -> list[list[int]]:
    """Load the topography data from the file as list of list of ints."""
    return read_lines_as_list(fp, split="every", inst=int)


def get_trailhead_score(topography: list[list[int]], head: Position) -> Positions:
    """Given a trail starting at head, calculate the score number of valid paths starting at head."""
    curr_val = topography[head[0]][head[1]]
    reachable: Positions = set()

    if curr_val == 9:
        return {head}

    for neigh_dist in directions:
        neigh_pos = tuple_add_tuple(head, neigh_dist)

        # skip if new position is out of bounds
        if (
            neigh_pos[0] < 0
            or neigh_pos[0] >= len(topography)
            or neigh_pos[1] < 0
            or neigh_pos[1] >= len(topography[0])
        ):
            continue

        if topography[neigh_pos[0]][neigh_pos[1]] == curr_val + 1:
            reachable = reachable.union(get_trailhead_score(topography, head=neigh_pos))

    return reachable


def get_trailhead_rating(topography: list[list[int]], head: Position) -> int:
    """Given a trail starting at head, calculate the score number of valid paths starting at head."""
    curr_val = topography[head[0]][head[1]]
    reachable: int = 0

    if curr_val == 9:
        return 1

    for neigh_dist in directions:
        neigh_pos = tuple_add_tuple(head, neigh_dist)

        # skip if new position is out of bounds
        if (
            neigh_pos[0] < 0
            or neigh_pos[0] >= len(topography)
            or neigh_pos[1] < 0
            or neigh_pos[1] >= len(topography[0])
        ):
            continue

        if topography[neigh_pos[0]][neigh_pos[1]] == curr_val + 1:
            reachable += get_trailhead_rating(topography, head=neigh_pos)

    return reachable


def part1(topography: list[list[int]]) -> int:
    """Part1: Get the total score of all trailheads."""
    total = 0
    # find all 0s
    for i, row in enumerate(topography):
        for j, val in enumerate(row):
            if val == 0:
                total += len(get_trailhead_score(topography, head=(i, j)))
    return total


def part2(topography: list[list[int]]) -> int:
    """Part2: Get the total rating of all trailheads."""
    total = 0
    # find all 0s
    for i, row in enumerate(topography):
        for j, val in enumerate(row):
            if val == 0:
                total += get_trailhead_rating(topography, head=(i, j))
    return total


class Test2024Day10(unittest.TestCase):

    fp = "./data/10-test.txt"
    test_data = load_data(fp)

    fp_2 = "./data/10-test-2.txt"
    test_data_2 = load_data(fp_2)

    def test_get_trailhead_score(self):
        for topography, head, result in [
            ([list(range(0, 10))], (0, 0), 1),
            (self.test_data_2, (0, 1), 1),
            (self.test_data_2, (6, 5), 2),
            (self.test_data, (0, 2), 5),
            (self.test_data, (0, 4), 6),
            (self.test_data, (2, 4), 5),
        ]:
            with self.subTest(
                msg="topography: {}, head: {}, result: {}".format(
                    topography, head, result
                )
            ):
                self.assertEqual(
                    len(get_trailhead_score(topography=topography, head=head)),
                    result,
                )

    def test_get_trailhead_rating(self):
        for topography, head, result in [
            ([list(range(0, 10))], (0, 0), 1),
            (self.test_data_2, (0, 1), 1),
            (self.test_data_2, (6, 5), 2),
            (self.test_data, (0, 2), 20),
            (self.test_data, (0, 4), 24),
            (self.test_data, (2, 4), 10),
        ]:
            with self.subTest(
                msg="topography: {}, head: {}, result: {}".format(
                    topography, head, result
                )
            ):
                self.assertEqual(
                    get_trailhead_rating(topography=topography, head=head),
                    result,
                )

    def test_p1(self):
        self.assertEqual(part1(self.test_data), 36)

    def test_p1_2(self):
        self.assertEqual(part1(self.test_data_2), 3)

    def test_p1_real(self):
        self.assertEqual(part1(load_data("./data/10.txt")), 825)

    def test_p2(self):
        self.assertEqual(part2(self.test_data), 81)

    def test_p2_2(self):
        self.assertEqual(part2(self.test_data_2), 3)


if __name__ == "__main__":
    print(">>> Start Main 10:")
    puzzle_data = load_data("./data/10.txt")
    print("Part 1): ", part1(puzzle_data))
    print("Part 2): ", part2(puzzle_data))
    print("End Main 10<<<")
