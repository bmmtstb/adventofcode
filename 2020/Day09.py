import unittest
from typing import List, Set


def load(filepath: str) -> List[int]:
    """load the file"""
    data = []
    with open(filepath) as file:
        for l in file.readlines():
            data.append(int(l))
    return data


def find_not_matching(data: List[int], n: int = 25, nof_prev_nums: int = 2) -> int:
    """Find fist number in list, which is not a sum of previous numbers"""
    # start after preamble
    for i in range(n, len(data)):
        if data[i] not in sum_of_different_n(data[i - n:i], nof_prev_nums):
            return data[i]
    return -1


def sum_of_different_n(data: List[int], n=2) -> Set[int]:
    """for every point in the data, calculate the sum of n different numbers"""
    if n == 1:
        return set(data)
    sums = []
    for i in range(len(data)):
        for j in sum_of_different_n(data[:i] + data[i + 1:], n - 1):
            sums.append(int(data[i] + j))
    return set(sums)


def find_continuous_sum(data: List[int], goal: int) -> List[int]:
    """Search a data string for a continuous list of numbers that sum to goal"""
    for i in range(len(data)):
        n = 1
        current_sum = data[i]
        while current_sum <= goal:
            if current_sum == goal:
                return data[i:i + n]
            n += 1
            current_sum = sum(data[i:i + n])
    return []


class Test2020Day09(unittest.TestCase):
    def test_sum_of_n(self):
        for d, n, res in [
            [[1, 2, 3], 2, {3, 4, 5}],
            [[1, 2, 3], 3, {6}],
            [[1, 2, 3, 4], 3, {6, 7, 8, 9}],
        ]:
            with self.subTest():
                self.assertEqual(sum_of_different_n(d, n), res)

    def test_find_not_matching(self):
        data = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]
        self.assertEqual(find_not_matching(data, 5), 127)

    def test_find_continuous_sum(self):
        data = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]
        cont = [15, 25, 47, 40]
        self.assertEqual(find_continuous_sum(data, 127), cont)


if __name__ == '__main__':
    print(">>> Start Main 09:")
    puzzle_input = load("data/09.txt")
    print("Part 1):")
    err = find_not_matching(puzzle_input)
    print(err)
    print("Part 2):")
    cont = find_continuous_sum(puzzle_input, err)
    print(cont)
    print(min(cont) + max(cont))
    print("End Main 09<<<")
