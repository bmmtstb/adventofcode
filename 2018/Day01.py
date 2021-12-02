import unittest
from parameterized import parameterized
from typing import Dict, List, Tuple, Set

from helper.data_helper import read_lines_as_list


def cumulate_frequency_change(l: List[int]) -> int:
    """From a given list of frequency changes, calculate resulting frequency"""
    return sum(change for change in l)


def find_recurring_frequency(l: List[int]) -> int:
    """iterate thorugh the list (multiple times) until a frequency is reached twice"""
    frequencies = []
    val = 0
    curr_l = l.copy()
    while True:
        val += curr_l.pop(0)
        if val in frequencies:
            return val
        else:
            frequencies.append(val)
        if len(curr_l) == 0:
            curr_l += l


class Test2018Day01(unittest.TestCase):
    @parameterized.expand([
        [[+1, -2, +3, +1], 3],
        [[+1, +1, +1], 3],
        [[+1, +1, -2], 0],
        [[-1, -2, -3], -6],
    ])
    def test_cumulate(self, freq_change, res):
        self.assertEqual(cumulate_frequency_change(freq_change), res)

    @parameterized.expand([
        [[+1, -2, +3, +1], 2],
        [[+1, +1, -2], 1],
        [[+1, -1], 1],
        [[+3, +3, +4, -2, -4], 10],
        [[- 6, +3, +8, +5, -6], 5],
        [[+7, +7, -2, -7, -4], 14],
    ])
    def test_recurring(self, freq_change, rec):
        self.assertEqual(find_recurring_frequency(freq_change), rec)


if __name__ == '__main__':
    print(">>> Start Main 01:")
    puzzle_input = read_lines_as_list("data/01.txt", t=int)
    print("Part 1): ", cumulate_frequency_change(puzzle_input))
    print("Part 2): ", find_recurring_frequency(puzzle_input))
    print("End Main 01<<<")
