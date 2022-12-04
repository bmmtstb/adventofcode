import unittest
from typing import Dict, List, Tuple, Set
from helper.file import read_lines_as_list


def find_increasing(l: List[int]) -> int:
    """in a list of integers find increasing ones"""
    return sum(1 if l[i] < l[i+1] else 0 for i in range(len(l)-1))


def create_sliding_window_list(l: List[int], size: int = 3) -> List[int]:
    """for a given list, slide a window of given size and sum all the values in the window"""
    return [sum(l[pos + i] for i in range(size)) for pos in range(len(l) - size + 1)]


class Test2021Day01(unittest.TestCase):
    draft = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

    def test_increasing(self):
        for data, incr in [
            [self.draft, 7],
            [[607, 618, 618, 617, 647, 716, 769, 792], 5]
        ]:
            with self.subTest():
                self.assertEqual(find_increasing(data), incr)

    def test_sliding_list(self):
        self.assertEqual(create_sliding_window_list(self.draft), [607, 618, 618, 617, 647, 716, 769, 792])


if __name__ == '__main__':
    print(">>> Start Main 01:")
    puzzle_input = read_lines_as_list("data/01.txt", int)
    print("Part 1): ", find_increasing(puzzle_input))
    print("Part 2):", find_increasing(create_sliding_window_list(puzzle_input)))
    print("End Main 01<<<")
