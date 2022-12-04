import unittest
from typing import Dict, List, Tuple, Set

from helper.file import read_lines_as_list
from Day05 import run_intcode_program


# Directions
# north (1), south (2), west (3), and east (4)
dirs = {
    1: (0,  1),
    2: (0, -1),
    3: (-1, 0),
    4: (1,  0)
}


def find_shortest_path(
        program: List[int],
        valid_programs: List[List[int]]
) -> (int, List[int]):
    """find the length of the shortest path by generating all paths with length n"""
    new_valid_programs = []
    for valid in valid_programs:
        for curr_dir in dirs.keys():
            new_input = valid + [curr_dir]
            outp, _, _, _ = run_intcode_program(program, new_input)
            # Status (output[0])
            # 0: The repair droid hit a wall. Its position has not changed.
            # 1: The repair droid has moved one step in the requested direction.
            # 2: The repair droid has moved one step in the requested direction; new pos == oxygen system pos.
            if outp:  # 1 or 2
                # add new found program to possible descendants
                new_valid_programs.append(new_input)
                if outp == 2:
                    return len(new_input), new_input
    return find_shortest_path(program, new_valid_programs)


class Test2019Day15(unittest.TestCase):
    pass


if __name__ == '__main__':
    print(">>> Start Main 15:")
    program = read_lines_as_list("data/15.txt")
    i, path = find_shortest_path(program, [[]])
    print("Part 1):")
    print(i)
    print("Part 2):")
    print("End Main 15<<<")
