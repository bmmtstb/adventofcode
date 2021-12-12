import unittest
from copy import deepcopy

from parameterized import parameterized
from typing import Dict, List, Tuple, Set

from helper.file import read_lines_as_list


def load_data(filepath: str) -> Dict[str, List[str]]:
    """Load paths - bidirectional"""
    lines = read_lines_as_list(filepath, split="-")
    possible_paths: Dict[str, List[str]] = {}
    for line in lines:
        if line[0] in possible_paths.keys():
            possible_paths[line[0]].append(line[1])
        else:
            possible_paths[line[0]] = [line[1]]
        # bidirectional
        if line[1] in possible_paths.keys():
            possible_paths[line[1]].append(line[0])
        else:
            possible_paths[line[1]] = [line[0]]
    return possible_paths


def generate_possible_paths(cave_system: Dict[str, List[str]], start: str = "start", end: str = "end",
                            init_path: List[str] = None, single_multiple_times: bool = False) -> List[List[str]]:
    """given a start and end node, calculate every distinct path from s to e. Small caves may not be visited twice"""
    if init_path is None:
        init_path = [start]
    possible_paths = []

    for next_node in cave_system[start]:
        # never visit start twice
        if next_node == "start":
            continue

        # reset curr path to init
        curr_path = [] if init_path is None else deepcopy(init_path)

        # special case - small cave
        # if small caves may be visited once don't add path if small cave was visited
        # if second task, one small cave may be visited twice throughout path
        if next_node.islower() and next_node in curr_path and (
                (
                    not single_multiple_times
                ) or (
                    # case part 2 -> cont if char is in path iff no char appears twice already
                    single_multiple_times and any(curr_path.count(pos) > 1 for pos in curr_path if pos.islower())
                )
        ):
            continue

        # append next to path
        curr_path.append(next_node)
        # end if end is found
        if next_node == end:
            # save curr and reset curr
            possible_paths.append(curr_path)
            continue
        # recursively call for next node
        sub_possibilities = generate_possible_paths(cave_system, start=next_node, init_path=deepcopy(curr_path),
                                                    end=end, single_multiple_times=single_multiple_times)
        possible_paths += sub_possibilities

    return possible_paths


class Test2021Day12(unittest.TestCase):
    @parameterized.expand([
        ["data/12-short.txt", 10, False],
        ["data/12-test.txt", 19, False],
        ["data/12-larger.txt", 226, False],
        ["data/12-short.txt", 36, True],
        ["data/12-test.txt", 103, True],
        ["data/12-larger.txt", 3509, True],

    ])
    def test_distinct_length(self, fp, nof, smt):
        poss_path = load_data(fp)
        self.assertEqual(len(generate_possible_paths(poss_path, single_multiple_times=smt)), nof)


if __name__ == '__main__':
    print(">>> Start Main 12:")
    puzzle_input = load_data("data/12.txt")
    print("Part 1): ", len(generate_possible_paths(deepcopy(puzzle_input))))
    print("Part 2): ", len(generate_possible_paths(deepcopy(puzzle_input), single_multiple_times=True)))
    print("End Main 12<<<")
