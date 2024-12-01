import unittest
from typing import Dict, List, Tuple, Set


def get_nth_spoken(start: List[int], n: int) -> int:
    """play the elves game until char n"""
    start.reverse()
    state = start
    while len(state) < n:
        # does not exist yet
        if state.count(state[0]) == 1:
            state.insert(0, 0)
        # diff
        else:
            idx = state.index(state[0], 1)
            state.insert(0, idx)
    return state[0]


def get_nth_spoken_faster(start: List[int], n: int) -> int:
    """play the elves game in larger scale"""
    state = {}  # for every spoken key, save last index
    for i_start, val in enumerate(start[:-1]):
        state[val] = i_start + 1
    i = len(start)
    last_spoken = start[-1]
    while i < n:
        try:
            new_val = i - state[last_spoken]
            state[last_spoken] = i
            last_spoken = new_val
        except KeyError:
            state[last_spoken] = i
            last_spoken = 0
        i += 1
    return last_spoken


class Test2020Day15(unittest.TestCase):
    def test_nth_number(self):
        for start, n, res in [
            [[0, 3, 6], 4, 0],
            [[0, 3, 6], 5, 3],
            [[0, 3, 6], 6, 3],
            [[0, 3, 6], 7, 1],
            [[0, 3, 6], 8, 0],
            [[0, 3, 6], 9, 4],
            [[0, 3, 6], 10, 0],
            [[0, 3, 6], 2020, 436],
            [[1, 3, 2], 2020, 1],
            [[2, 1, 3], 2020, 10],
            [[1, 2, 3], 2020, 27],
            [[2, 3, 1], 2020, 78],
            [[3, 2, 1], 2020, 438],
            [[3, 1, 2], 2020, 1836],
        ]:
            with self.subTest():
                self.assertEqual(get_nth_spoken(start.copy(), n), res)

    def test_big_numbers(self):
        for start, n, res in [
            [[0, 3, 6], 4, 0],
            [[0, 3, 6], 5, 3],
            [[0, 3, 6], 6, 3],
            [[0, 3, 6], 7, 1],
            [[0, 3, 6], 8, 0],
            [[0, 3, 6], 9, 4],
            [[0, 3, 6], 10, 0],
            # [[0, 3, 6], 30000000, 175594],
            # [[1, 3, 2], 30000000, 2578],
            # [[2, 1, 3], 30000000, 3544142],
            # [[1, 2, 3], 30000000, 261214],
            # [[2, 3, 1], 30000000, 6895259],
            # [[3, 2, 1], 30000000, 18],
            # [[3, 1, 2], 30000000, 362],
        ]:
            with self.subTest():
                self.assertEqual(get_nth_spoken_faster(start.copy(), n), res)


if __name__ == "__main__":
    print(">>> Start Main 15:")
    puzzle_input = [12, 20, 0, 6, 1, 17, 7]
    print("Part 1):")
    print(get_nth_spoken(puzzle_input.copy(), 2020))
    print("Part 2):")
    print(get_nth_spoken_faster(puzzle_input.copy(), 30000000))
    print("End Main 15<<<")
