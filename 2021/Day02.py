import unittest
from parameterized import parameterized
from typing import Dict, List, Tuple, Set

from helper.tuple import tuple_add_tuple
from helper.file import read_lines_as_list


def follow_directions(dirs: List[List[str]]) -> Tuple[int, int]:
    """Follow a given set of directions"""
    pos: Tuple[int, int] = (0, 0)
    for dir in dirs:
        if dir[0] == "forward":
            pos = tuple_add_tuple(pos, (int(dir[1]), 0))
        elif dir[0] == "down":
            pos = tuple_add_tuple(pos, (0, int(dir[1])))
        elif dir[0] == "up":
            pos = tuple_add_tuple(pos, (0, -int(dir[1])))
        else:
            raise Exception("Unknown direction {}".format(dir[0]))
    return pos


def follow_directions_2(dirs: List[List[str]]) -> Tuple[int, int]:
    """Follow a given set of directions"""
    aim = 0
    pos: Tuple[int, int] = (0, 0)
    for dir in dirs:
        if dir[0] == "forward":
            pos = tuple_add_tuple(pos, (int(dir[1]), aim * int(dir[1])))
        elif dir[0] == "down":
            aim += int(dir[1])
        elif dir[0] == "up":
            aim -= int(dir[1])
        else:
            raise Exception("Unknown direction {}".format(dir[0]))
    return pos


class Test2021Day02(unittest.TestCase):
    @parameterized.expand([
        [[["forward", "5"], ["down", "5"], ["forward", "8"], ["up", "3"], ["down", "8"], ["forward", "2"]], (15, 10)],
    ])
    def test_follow_dirs(self, dirs, fin):
        self.assertTupleEqual(follow_directions(dirs), fin)

    @parameterized.expand([
        [[["forward", "5"], ["down", "5"], ["forward", "8"], ["up", "3"], ["down", "8"], ["forward", "2"]], (15, 80)],
    ])
    def test_follow_dirs_2(self, dirs, fin):
        self.assertTupleEqual(follow_directions(dirs), fin)


if __name__ == '__main__':
    print(">>> Start Main 02:")
    puzzle_input = read_lines_as_list("data/02.txt", split=" ")
    p_final = follow_directions(puzzle_input)
    print("Part 1): ", p_final, " -> ", p_final[0] * p_final[1])
    p_final_2 = follow_directions_2(puzzle_input)
    print("Part 2): ", p_final_2, " -> ", p_final_2[0] * p_final_2[1])
    print("End Main 02<<<")
