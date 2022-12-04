import unittest
from typing import Dict, List, Tuple, Set
from copy import deepcopy

from helper.file import read_lines_as_list
from helper.tuple import tuple_add_tuple

pos = Tuple[int, int]

adjacent: List[Tuple[int, int]] = [
    (1, 1),
    (1, 0),
    (0, 1),
    (-1, -1),
    (-1, 0),
    (0, -1),
    (-1, 1),
    (1, -1)
]


def flash_octopus(position: pos, curr_map: List[List[int]], already_flashed: List[pos]) -> int:
    """flash an octopus at position, call recursive if necessary"""
    nof_flashes = 0
    # octopus can flash once every time-step
    if position not in already_flashed:
        # append to flashed and flash
        already_flashed.append(position)
        nof_flashes += 1
        # add +1 to all 8 adjacent octopus
        for adj in adjacent:
            neighbor = tuple_add_tuple(position, adj)
            # if neighbor on board increase
            if 0 <= neighbor[0] < 10 and 0 <= neighbor[1] < 10:
                curr_map[neighbor[1]][neighbor[0]] += 1
                # if this changed neighbor above threshold, call recursive
                if curr_map[neighbor[1]][neighbor[0]] > 9:
                    sub_flashes = flash_octopus(neighbor, curr_map, already_flashed)
                    nof_flashes += sub_flashes
    return nof_flashes


def model_octopus(curr_map: List[List[int]], steps: int) -> (List[List[int]], int):
    """model energy level of each octopus and predict flashes, return updated board and nof flashes"""
    """"
    1) The energy level of each octopus increases by 1.
    2) Any octopus with an energy level greater than 9 flashes. This increases the energy level of all adjacent
    octopuses by 1, including octopuses that are diagonally adjacent. If this causes an octopus to have an energy level
    greater than 9, it also flashes. This process continues as long as new octopuses keep having their energy level
    increased beyond 9. (An octopus can only flash at most once per step.)
    3) Any octopus that flashed during this step has its energy level set to 0, as it used all of its energy to flash.
    """
    flashes = 0
    for i in range(steps):
        # no flashes in beginning of step
        flashed_in_step: List[pos] = []
        # 1) increase level by 1
        for y in range(len(curr_map)):
            for x in range(len(curr_map[0])):
                curr_map[y][x] += 1
                # 2) search for val > 9
                if curr_map[y][x] > 9:
                    # update map and pos_flashed on the fly
                    new_flashes = flash_octopus((x, y), curr_map, flashed_in_step)
                    flashes += new_flashes
        # 3) set every pos in flashed_in_step to 0
        for position in flashed_in_step:
            curr_map[position[1]][position[0]] = 0
    return curr_map, flashes


def did_synchronise(curr_map: List[List[int]]) -> int:
    """Check if all octopus have synchronized"""
    i = 0
    while not all(all(val == curr_map[0][0] for val in line) for line in curr_map):
        model_octopus(curr_map, 1)
        i += 1
    return i


class Test2021Day11(unittest.TestCase):
    test_data = [[int(val) for val in line] for line in read_lines_as_list("data/11-test.txt", list)]

    def test_nof_flashes(self):
        for steps, flashes, board in [
            [1, 0, [
                [6, 5, 9, 4, 2, 5, 4, 3, 3, 4],
                [3, 8, 5, 6, 9, 6, 5, 8, 2, 2],
                [6, 3, 7, 5, 6, 6, 7, 2, 8, 4],
                [7, 2, 5, 2, 4, 4, 7, 2, 5, 7],
                [7, 4, 6, 8, 4, 9, 6, 5, 8, 9],
                [5, 2, 7, 8, 6, 3, 5, 7, 5, 6],
                [3, 2, 8, 7, 9, 5, 2, 8, 3, 2],
                [7, 9, 9, 3, 9, 9, 2, 2, 4, 5],
                [5, 9, 5, 7, 9, 5, 9, 6, 6, 5],
                [6, 3, 9, 4, 8, 6, 2, 6, 3, 7]]],
            [10, 204, [
                [0, 4, 8, 1, 1, 1, 2, 9, 7, 6],
                [0, 0, 3, 1, 1, 1, 2, 0, 0, 9],
                [0, 0, 4, 1, 1, 1, 2, 5, 0, 4],
                [0, 0, 8, 1, 1, 1, 1, 4, 0, 6],
                [0, 0, 9, 9, 1, 1, 1, 3, 0, 6],
                [0, 0, 9, 3, 5, 1, 1, 2, 3, 3],
                [0, 4, 4, 2, 3, 6, 1, 1, 3, 0],
                [5, 5, 3, 2, 2, 5, 2, 3, 5, 0],
                [0, 5, 3, 2, 2, 5, 0, 6, 0, 0],
                [0, 0, 3, 2, 2, 4, 0, 0, 0, 0]]],
            [100, 1656, [
                [0, 3, 9, 7, 6, 6, 6, 8, 6, 6],
                [0, 7, 4, 9, 7, 6, 6, 9, 1, 8],
                [0, 0, 5, 3, 9, 7, 6, 9, 3, 3],
                [0, 0, 0, 4, 2, 9, 7, 8, 2, 2],
                [0, 0, 0, 4, 2, 2, 9, 8, 9, 2],
                [0, 0, 5, 3, 2, 2, 2, 8, 7, 7],
                [0, 5, 3, 2, 2, 2, 2, 9, 6, 6],
                [9, 3, 2, 2, 2, 2, 8, 9, 6, 6],
                [7, 9, 2, 2, 2, 8, 6, 8, 6, 6],
                [6, 7, 8, 9, 9, 9, 8, 7, 6, 6]]],
        ]:
            with self.subTest():
                updated_data, measured_flashes = model_octopus(deepcopy(self.test_data), steps)
                self.assertEqual(measured_flashes, flashes)
                self.assertEqual(updated_data, board)

    def test_example_board(self):
        test_data2 = [[1, 1, 1, 1, 1],
                      [1, 9, 9, 9, 1],
                      [1, 9, 1, 9, 1],
                      [1, 9, 9, 9, 1],
                      [1, 1, 1, 1, 1]]
        updated_data, measured_flashes = model_octopus(deepcopy(test_data2), 1)
        test_solution = [[3, 4, 5, 4, 3],
                         [4, 0, 0, 0, 4],
                         [5, 0, 0, 0, 5],
                         [4, 0, 0, 0, 4],
                         [3, 4, 5, 4, 3]]
        self.assertEqual(measured_flashes, 9)
        self.assertEqual(test_solution, updated_data)

    def test_synchronising(self):
        self.assertEqual(did_synchronise(deepcopy(self.test_data)), 195)


if __name__ == '__main__':
    print(">>> Start Main 11:")
    puzzle_input = [[int(val) for val in line] for line in read_lines_as_list("data/11.txt", list)]
    updated_puzzle, puzzle_flashes = model_octopus(deepcopy(puzzle_input), 100)
    print("Part 1): ", puzzle_flashes)
    print("Part 2): ", did_synchronise(deepcopy(puzzle_input)))
    print("End Main 11<<<")
