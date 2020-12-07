import unittest

from parameterized import parameterized
from itertools import groupby

puzzle_input = (136818, 685979)


def criteria_six_digit(num):
    """Returns true if a number has six digits"""
    return 100000 <= num < 1000000


def criteria_within_puzzle_input(num):
    """Returns true if a number is in a specific range of numbers"""
    return num in range(*puzzle_input)


def criteria_two_adjacent_digits(num):
    """Returns true if the number contains two adjacent digits"""
    num = str(num)
    return any(int(num[i]) == int(num[i+1]) for i in range(len(num)-1))


def criteria_non_decreasing_sequence(num):
    """Returns true if the number does not contain a decreasing sequence"""
    num = str(num)
    return all(int(num[i+1]) >= int(num[i]) for i in range(len(num)-1))


def criteria_no_larger_group(num):
    """Returns true if the number does contain a pair of digits that are equal, but not part of a bigger group"""
    return any(len(list(v)) == 2 for _, v in groupby(str(num)))


def number_meets_criteria_1(num):
    """Returns true if a number meets all the given criteria for part 1"""
    return all([criteria_non_decreasing_sequence(num), criteria_two_adjacent_digits(num),
                criteria_within_puzzle_input(num), criteria_six_digit(num)])


def number_meets_criteria_2(num):
    """Returns true if a number meets all the given criteria for part 1"""
    return all([criteria_non_decreasing_sequence(num), criteria_two_adjacent_digits(num),
                criteria_within_puzzle_input(num), criteria_six_digit(num), criteria_no_larger_group(num)])


def how_many_correct_in_puzzle_range(part):
    """Returns the number of correct numbers withing puzzle_range"""
    if part == 1:
        return sum(1 for num in range(*puzzle_input) if number_meets_criteria_1(num))
    elif part == 2:
        return sum(1 for num in range(*puzzle_input) if number_meets_criteria_2(num))


class Test2019Day04(unittest.TestCase):
    @parameterized.expand([
        [1, False],
        [100000, True],
        [-100000, False],
    ])
    def test_criteria_digits(self, number, meets):
        self.assertEqual(criteria_six_digit(number), meets)

    @parameterized.expand([
        [136818, True],
        [100000, False],
        [685979, False],
    ])
    def test_criteria_range(self, number, meets):
        self.assertEqual(criteria_within_puzzle_input(number), meets)

    @parameterized.expand([
        [100000, True],
        [101010, False],
        [122345, True],
        [123789, False],
    ])
    def test_criteria_adjacent(self, number, meets):
        self.assertEqual(criteria_two_adjacent_digits(number), meets)

    @parameterized.expand([
        [100000, False],
        [111123, True],
        [135679, True],
        [223450, False],
    ])
    def test_criteria_non_decreasing(self, number, meets):
        self.assertEqual(criteria_non_decreasing_sequence(number), meets)

    @parameterized.expand([
        [100000, False],
        [101010, False],
        [122345, True],
        [122245, False],
        [111122, True],
        [122325, True],
    ])
    def test_criteria_no_larger_group(self, num, meets):
        self.assertEqual(criteria_no_larger_group(num), meets)


if __name__ == '__main__':
    print("1: ", how_many_correct_in_puzzle_range(1))
    print("2: ", how_many_correct_in_puzzle_range(2))
