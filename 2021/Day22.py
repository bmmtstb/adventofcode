import unittest
from typing import List, Tuple, Set

from helper.file import read_lines_as_list

Range = Tuple[int, int]
Cuboid = Tuple[bool, Range, Range, Range]


def load_data(filepath: str) -> List[Cuboid]:
    """load data from file"""
    ranges_list = []
    for line in read_lines_as_list(filepath):
        turn, ranges = line.split(" ")
        turn = True if turn == "on" else False
        x, y, z = ranges.split(",")
        x: Range = tuple(int(i) for i in x[2:].split("..")[:2])
        y: Range = tuple(int(i) for i in y[2:].split("..")[:2])
        z: Range = tuple(int(i) for i in z[2:].split("..")[:2])
        if any(r[0] <= r[1] for r in [x, y, z]):
            raise Exception("first value should be smaller than second.")
        ranges_list.append((turn, x, y, z))
    return ranges_list


def get_shape_from_range(ranges: Tuple[Range, Range, Range]) -> Tuple[int, int, int]:
    """given a set of ranges, calculate the size"""
    return (
        ranges[0][1] - ranges[0][0] + 1,
        ranges[1][1] - ranges[1][0] + 1,
        ranges[2][1] - ranges[2][0] + 1,
    )


def split_into_cubes(cub_pos: Cuboid, cub_neg: Cuboid) -> Set[Cuboid]:
    """Given a positive cube, split that cube into multiple smaller cubes excluding the negative one"""
    new_cubes: Set[Cuboid] = set()
    # Range = (lower, upper)
    # Cuboid = bool, 3x Range
    # never accept Cuboids with negative difference between lower and upper
    for i in range(1, 4):
        # everything before the current index uses max(lower_pos, lower_neg) and min(upper_pos, upper_neg)
        before = tuple(
            tuple(
                [max(cub_pos[b][0], cub_neg[b][0]), min(cub_pos[b][1], cub_neg[b][1])]
            )
            for b in range(1, i)
        )
        if any(tup[0] <= tup[1] for tup in before):
            raise Exception("first value should be smaller than second")
        # indices after the current always give (lower_pos, upper_pos)
        after = tuple(cub_pos[a] for a in range(i + 1, 4))
        if any(tup[0] <= tup[1] for tup in after):
            raise Exception("first value should be smaller than second")
        # the current index provides two possible new areas, (lower_pos, lower_neg - 1) and (upper_neg + 1, upper_pos)
        curr = []
        if cub_neg[i][0] - 1 >= cub_pos[i][0]:
            curr.append((cub_pos[i][0], cub_neg[i][0] - 1))
        if cub_neg[i][1] + 1 <= cub_pos[i][1]:
            curr.append((cub_neg[i][1] + 1, cub_pos[i][1]))
        # the new areas are the concatenations of before, curr, after, with all possible permutations of curr (max 2 atm)
        for c in curr:
            new_cube = tuple([True]) + before + tuple([c]) + after
            new_cubes.add(new_cube)
    return new_cubes


def are_cubes_intersecting(cub1: Cuboid, cub2: Cuboid) -> bool:
    """Return whether two cubes are intersecting"""
    # completely outside
    if any(
        cub1[dim][0] > cub2[dim][1] or cub1[dim][1] < cub2[dim][0]
        for dim in range(1, 4)
    ):
        return False
    return True


def is_cube_subset(cub1: Cuboid, cub2: Cuboid) -> bool:
    """Return whether cube 2 is completely inside of cube 1"""
    return all(
        cub1[dim][0] <= cub2[dim][0] and cub1[dim][1] >= cub2[dim][1]
        for dim in range(1, 4)
    )


def count_active(steps: List[Cuboid], initialization: bool = False) -> int:
    """count how many positions are active for a list of conditions"""
    act_cubes: Set[Cuboid] = set()  # list of active cube segments
    for step in steps:
        # with init ignore everything out of range (-50, 50)
        if initialization and any(
            step[i][0] < -50 or step[i][1] > 50 for i in range(1, 4)
        ):
            continue
        # check for intersection with already existing cubes
        # on - make sure no duplicates
        # off - remove inactive part
        new_cubes = set()
        remove_cubes = set()
        for act_cube in act_cubes:
            if are_cubes_intersecting(act_cube, step):
                new_cubes = new_cubes.union(split_into_cubes(act_cube, step))
                remove_cubes.add(act_cube)
        act_cubes = act_cubes.union(new_cubes)
        act_cubes = act_cubes.difference(remove_cubes)
        if step[0]:  # if on : remove current then add current as complete
            act_cubes.add(step)
    # active is just sum of (w * h * d) of every cuboid
    # +1 : Cube w range (0, 0) still is 1 Element wide
    return sum(
        (cube[1][1] - cube[1][0] + 1)
        * (cube[2][1] - cube[2][0] + 1)
        * (cube[3][1] - cube[3][0] + 1)
        for cube in act_cubes
    )


class Test2021Day22(unittest.TestCase):

    def test_intersecting(self):
        for b1, b2, b in [
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (True, (0, 10), (0, 10), (0, 10)),
                True,
            ],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (True, (10, 11), (10, 11), (10, 11)),
                True,
            ],
            [(True, (0, 10), (0, 10), (0, 10)), (True, (1, 1), (4, 4), (3, 3)), True],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (True, (-10, -1), (-10, -1), (-2, -1)),
                False,
            ],
            [(True, (0, 10), (0, 10), (0, 10)), (True, (1, 2), (3, 4), (5, 6)), True],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (True, (-2, -1), (-10, -1), (4, 100)),
                False,
            ],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (True, (-2, -1), (10, 100), (-10, -1)),
                False,
            ],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (True, (-100, 100), (-2, -1), (-10, -1)),
                False,
            ],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (True, (11, 12), (-2, -1), (11, 14)),
                False,
            ],
            [
                (True, (11, 12), (10, 10), (10, 12)),
                (True, (10, 10), (10, 10), (10, 10)),
                False,
            ],
            [
                (True, (11, 12), (10, 10), (10, 12)),
                (False, (9, 11), (9, 11), (9, 11)),
                True,
            ],
        ]:
            with self.subTest(msg=f"b1={b1},b2={b2},b={b}"):
                self.assertEqual(are_cubes_intersecting(b1, b2), b)

    def test_subset(self):
        for b1, b2, b in [
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (True, (0, 10), (0, 10), (0, 10)),
                True,
            ],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (True, (10, 10), (10, 10), (10, 10)),
                True,
            ],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (True, (10, 11), (10, 11), (10, 11)),
                False,
            ],
            [(True, (0, 10), (0, 10), (0, 10)), (True, (1, 1), (4, 4), (3, 3)), True],
            [(True, (0, 10), (0, 10), (0, 10)), (True, (0, 0), (4, 4), (10, 10)), True],
            [(True, (0, 10), (0, 10), (0, 10)), (True, (1, 2), (3, 4), (5, 6)), True],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (True, (-10, -1), (-10, -1), (-2, -1)),
                False,
            ],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (True, (-2, -1), (-10, -1), (4, 100)),
                False,
            ],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (True, (-2, -1), (10, 100), (-10, -1)),
                False,
            ],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (True, (-100, 100), (-2, -1), (-10, -1)),
                False,
            ],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (True, (11, 12), (-2, -1), (11, 14)),
                False,
            ],
        ]:
            with self.subTest(msg=f"b1={b1},b2={b2},b={b}"):
                self.assertEqual(is_cube_subset(b1, b2), b)

    def test_split_into_cubes(self):
        for c1, c2, cubes in [
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (False, (0, 10), (0, 10), (0, 10)),
                set(),
            ],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (False, (-1, 11), (-1, 11), (-10, 100)),
                set(),
            ],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (False, (0, 1), (0, 1), (0, 1)),
                {  # subset with cuts at border
                    # (True, (0, -1), (0, 10), (0, 10)),
                    (True, (2, 10), (0, 10), (0, 10)),
                    # (True, (0, 1), (0, -1), (0, 10)),
                    (True, (0, 1), (2, 10), (0, 10)),
                    # (True, (0, 1), (0, 1), (0, -1)),
                    (True, (0, 1), (0, 1), (2, 10)),
                },
            ],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (False, (2, 4), (-100, 100), (-100, 100)),
                {
                    (True, (0, 1), (0, 10), (0, 10)),
                    (True, (5, 10), (0, 10), (0, 10)),
                    # (True, (2, 4), (-100, 100), (0, 10)),
                    # (True, (2, 4), (-100, 100), (0, 10)),
                    # (True, (2, 4), (2, 4), (-100, 100)),
                    # (True, (2, 4), (2, 4), (-100, 100)),
                },
            ],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (False, (-100, 100), (2, 4), (-100, 100)),
                {
                    # (True, (-100, 100), (0, 10), (0, 10)),
                    # (True, (-100, 100), (0, 10), (0, 10)),
                    (True, (0, 10), (0, 1), (0, 10)),
                    (True, (0, 10), (5, 10), (0, 10)),
                    # (True, (0, 10), (2, 4), (-100, 100)),
                    # (True, (0, 10), (2, 4), (-100, 100)),
                },
            ],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (False, (-100, 100), (-100, 4), (-100, 100)),
                {
                    # (True, (-100, 100), (0, 10), (0, 10)),
                    # (True, (-100, 100), (0, 10), (0, 10)),
                    # (True, (0, 10), (0, -101), (0, 10)),
                    (True, (0, 10), (5, 10), (0, 10)),
                    # (True, (0, 10), (2, 4), (-100, 100)),
                    # (True, (0, 10), (2, 4), (-100, 100)),
                },
            ],
            [
                (True, (0, 10), (0, 10), (0, 10)),
                (False, (1, 2), (3, 4), (5, 6)),
                {  # subset
                    (True, (0, 0), (0, 10), (0, 10)),
                    (True, (3, 10), (0, 10), (0, 10)),
                    (True, (1, 2), (0, 2), (0, 10)),
                    (True, (1, 2), (5, 10), (0, 10)),
                    (True, (1, 2), (3, 4), (0, 4)),
                    (True, (1, 2), (3, 4), (7, 10)),
                },
            ],
            [
                (True, (10, 10), (10, 12), (10, 12)),
                (False, (9, 11), (9, 11), (9, 11)),
                {
                    # (True, (10, 8), (), ()),
                    # (True, (12, 10), (), ()),
                    # (True, (10, 10), (10, 8), ()),
                    (True, (10, 10), (12, 12), (10, 12)),
                    # (True, (10, 10), (10, 11), (10, 8)),
                    (True, (10, 10), (10, 11), (12, 12)),
                },
            ],
        ]:
            with self.subTest():
                self.assertSetEqual(split_into_cubes(c1, c2), cubes)

    def test_count_active(self):
        conds = load_data("data/22-example.txt")
        self.assertEqual(count_active(conds, True), 39)

    def test_count_active_larger(self):
        conds = load_data("data/22-example-larger.txt")
        self.assertEqual(count_active(conds, True), 590784)

    def test_count_active_p2(self):
        conds = load_data("data/22-example-p2.txt")
        self.assertEqual(count_active(conds, True), 474140)


if __name__ == "__main__":
    print(">>> Start Main 22:")
    puzzle_conditions = load_data("data/22.txt")
    print("Part 1): ", count_active(puzzle_conditions.copy(), True))
    print("Part 2): ", count_active(puzzle_conditions.copy(), False))
    print("End Main 22<<<")
