import unittest
from typing import Dict, List, Tuple, Set

from helper.file import load_file_and_split


# INFO
# each lantern-fish creates a new lantern-fish once every 7 days -> not synced
def fish_lifecycle_list(
    init: List[int], nof_days: int, reproduction: int = 7, mature: int = 2
) -> List[int]:
    """follow the lanternfish lifecycle for n days"""
    curr_list = init.copy()
    for day in range(nof_days):
        # count new children
        new_childs = sum(1 if val == 0 else 0 for val in curr_list)
        #
        curr_list = [val - 1 if val > 0 else reproduction - 1 for val in curr_list]
        curr_list += [reproduction + mature - 1] * new_childs
    return curr_list


def fish_lifecycle_faster(
    init: List[int], nof_days: int, reproduction: int = 7, mature: int = 2
) -> int:
    """follow the lanternfish lifecycle for n days"""
    # save nof fishes of specific age in list
    nof_fishes_w_age = [0] * (reproduction + mature)
    # init
    for val in init:
        nof_fishes_w_age[val] += 1
    # loop
    for _ in range(nof_days):
        nof_mature_fish = nof_fishes_w_age.pop(0)
        nof_fishes_w_age[reproduction - 1] += nof_mature_fish
        nof_fishes_w_age.append(nof_mature_fish)
    return sum(val for val in nof_fishes_w_age)


class Test2021Day06(unittest.TestCase):
    def test_numbers(self):
        for days, l in [
            [1, [2, 3, 2, 0, 1]],
            [2, [1, 2, 1, 6, 0, 8]],
            [3, [0, 1, 0, 5, 6, 7, 8]],
            [5, [5, 6, 5, 3, 4, 5, 6, 7, 7, 8]],
            [10, [0, 1, 0, 5, 6, 0, 1, 2, 2, 3, 7, 8]],
            [15, [2, 3, 2, 0, 1, 2, 3, 4, 4, 5, 2, 3, 4, 4, 4, 5, 5, 6, 6, 7]],
            [
                18,
                [
                    6,
                    0,
                    6,
                    4,
                    5,
                    6,
                    0,
                    1,
                    1,
                    2,
                    6,
                    0,
                    1,
                    1,
                    1,
                    2,
                    2,
                    3,
                    3,
                    4,
                    6,
                    7,
                    8,
                    8,
                    8,
                    8,
                ],
            ],
        ]:
            with self.subTest():
                init_test = [3, 4, 3, 1, 2]
                self.assertListEqual(fish_lifecycle_list(init_test, days), l)

    def test_len(self):
        for days, nof in [
            [1, 5],
            [18, 26],
            [80, 5934],
        ]:
            with self.subTest():
                init_test = [3, 4, 3, 1, 2]
                self.assertEqual(len(fish_lifecycle_list(init_test, days)), nof)

    def test_faster_numbers(self):
        for days, nof in [[18, 26], [80, 5934], [256, 26984457539]]:
            with self.subTest():
                init_test = [3, 4, 3, 1, 2]
                self.assertEqual(fish_lifecycle_faster(init_test, days), nof)


if __name__ == "__main__":
    print(">>> Start Main 06:")
    puzzle_input = load_file_and_split("data/06.txt", ",", int)
    print("Part 1): ", fish_lifecycle_faster(puzzle_input.copy(), 80))
    print("Part 2): ", fish_lifecycle_faster(puzzle_input.copy(), 256))
    print("End Main 06<<<")
