import unittest
from parameterized import parameterized
from typing import List, Tuple
from copy import deepcopy

from helper.tuple_helper import tuple_add_tuple

mapping = {
    ".": -1,
    "L": 0,
    "#": 1,
}


def load(filepath: str) -> List[List[int]]:
    """load the file"""
    data = []
    with open(filepath) as file:
        for l in file.readlines():
            data.append(list(map(lambda c: mapping[c], l.replace("\n", ""))))
    return data


def change_seats_states(data: List[List[int]], seeing: bool = False) -> List[List[int]]:
    """Change all the seats simultaneously"""

    def adjacent_neighbors(r, c):
        """calculate the types of adjacent seats"""
        seeing_types = {-1: 0, 0: 0, 1: 0}
        directions = [(l, k) for k in range(-1, 2) for l in range(-1, 2) if not(l == k == 0)]
        for dire in directions:
            neigh_val = get_seen_in_direction((r, c), dire) if seeing else get_neighbor_in_direction((r, c), dire)
            if neigh_val:
                seeing_types[neigh_val] += 1
        return seeing_types

    def get_seen_in_direction(pos: Tuple[int, int], direction: Tuple[int, int]) -> int:
        """get the first seen seat in the direction"""
        i, j = tuple_add_tuple(pos, direction)
        while 0 <= i < len(data) and 0 <= j < len(data[i]):
            if data[i][j] >= 0:
                break
            else:
                i, j = tuple_add_tuple((i, j), direction)
        return data[i][j] if 0 <= i < len(data) and 0 <= j < len(data[i]) else None

    def get_neighbor_in_direction(pos: Tuple[int, int], direction: Tuple[int, int]) -> int:
        """get the neighboring element in the direction"""
        i, j = tuple_add_tuple(pos, direction)
        return data[i][j] if 0 <= i < len(data) and 0 <= j < len(data[i]) else None

    # (a) If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    # (b) If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    # (c) Otherwise, the seat's state does not change.
    new_data = deepcopy(data)
    for row_i, row in enumerate(data):
        for col_i, val in enumerate(row):
            # get neighboring values
            neighbors = adjacent_neighbors(row_i, col_i)
            # (a)
            if val == 0 and neighbors[1] == 0:
                new_data[row_i][col_i] = 1
            elif val == 1 and neighbors[1] >= (4 if not seeing else 5):
                new_data[row_i][col_i] = 0
            # state is already correct from copying
            # else:
            #     new_data[row_i][col_i] = val
    return new_data


def run_until_no_changes(data: List[List[int]], seeing: bool = False) -> List[List[int]]:
    """Change all the seats until the same state appears twice"""
    old_state = deepcopy(data)
    while True:
        state = change_seats_states(old_state, seeing)
        # if both states are equal
        if all(all(state[i][j] == old_state[i][j] for j in range(len(state[i]))) for i in range(len(data))):
            return old_state
        old_state = deepcopy(state)


def count_occupied_seats(data: List[List[int]]) -> int:
    """count how many seats are occupied"""
    return sum(sum(1 for val in r if val == 1) for r in data)


class Test2020Day11(unittest.TestCase):
    @parameterized.expand([
        ["data/11-test.txt", "data/11-test1.txt", False],
        ["data/11-test.txt", "data/11-test1.txt", True],
        ["data/11-test1.txt", "data/11-testS2.txt", True],
    ])
    def test_after_one_iteration(self, f1, f2, seeing):
        self.assertListEqual(change_seats_states(load(f1), seeing), load(f2))

    @parameterized.expand([
        ["data/11-test.txt", "data/11-testFin1.txt", 37, False],
        ["data/11-test.txt", "data/11-testFin2.txt", 26, True],
    ])
    def test_end_state(self, f1, f2, occ, see):
        end = run_until_no_changes(load(f1), see)
        self.assertListEqual(end, load(f2))
        self.assertEqual(count_occupied_seats(end), occ)


if __name__ == '__main__':
    print(">>> Start Main 11:")
    puzzle_input = load("data/11.txt")
    print("Part 1):")
    print(count_occupied_seats(run_until_no_changes(puzzle_input)))
    print("Part 2):")
    print(count_occupied_seats(run_until_no_changes(puzzle_input, seeing=True)))
    print("End Main 11<<<")
