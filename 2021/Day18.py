import unittest
from copy import deepcopy

from typing import Dict, List, Tuple, Set, Union, Iterable

from helper.file import read_lines_as_list

Pair = Tuple[int, int]
SnailFishNumber = Union[
    'Pair', Tuple['SnailFishNumber'], Tuple['Pair', 'SnailFishNumber'], Tuple['SnailFishNumber', 'Pair']]
Position = Union[None, List[int]]


class InvalidSFNIndexException(Exception):
    pass


def get_sfn(num: SnailFishNumber, num_pos: Position) -> Union[int, SnailFishNumber]:
    """get the value of a snail-fish number at a given pos"""
    try:
        if type(num) == int:
            raise InvalidSFNIndexException
        elif len(num_pos) == 1:
            return num[num_pos[0]]
        elif type(num_pos) == list:
            return get_sfn(num[num_pos[0]], num_pos[1:])
        else:
            raise Exception("Position is None")
    except IndexError:
        raise InvalidSFNIndexException


def set_sfn(num: SnailFishNumber, num_pos: Position, val: Union[int, SnailFishNumber]) -> SnailFishNumber:
    """set the position of a given snail-fish number to a given value"""
    try:
        if len(num_pos) == 0:
            return deepcopy(val)
        elif type(num_pos) == list:
            recursive_new = set_sfn(num[num_pos[0]], num_pos[1:], val)
            return (num[0], recursive_new) if num_pos[0] == 1 else (recursive_new, num[1])
    except IndexError:
        raise Exception("invalid position for snail-fish number.")


def find_first_left_number(num: SnailFishNumber, num_pos: Position) -> Position:
    """find the position of the first number to the left"""
    curr_pos = num_pos.copy()
    if 1 in curr_pos:  # if there is a 1, get the last one and change it to a 0
        curr_pos.reverse()
        idx = curr_pos.index(1)
        curr_pos = curr_pos[idx + 1:]
        curr_pos.reverse()
        curr_pos.append(0)
        # curr_pos is root of left-next branch, now get rightmost of this branch
        while True:
            try:
                curr_pos.append(1)
                get_sfn(num, curr_pos)
            except InvalidSFNIndexException:
                return curr_pos[:-1]
    # case no left neighbors
    return None


def find_first_right_number(num: SnailFishNumber, num_pos: Position) -> Position:
    """find the position of the first number to the right"""
    curr_pos = num_pos.copy()
    if 0 in curr_pos:  # if there is a 0, get the last one and change it to a 1
        curr_pos.reverse()
        idx = curr_pos.index(0)
        curr_pos = curr_pos[idx + 1:]
        curr_pos.reverse()
        curr_pos.append(1)
        # curr_pos is root of right-next branch, now get leftmost value of this branch
        while True:
            try:
                curr_pos.append(0)
                get_sfn(num, curr_pos)
            except InvalidSFNIndexException:
                return curr_pos[:-1]
    # case no right neighbors
    return None


def find_leftmost_pair_nested_multiple_times(num: SnailFishNumber, threshold: int = 4, depth: int = 1) -> Position:
    """return the leftmost pair with deeper nesting than threshold"""
    if any(type(val) == tuple for val in num):  # always get deepest nested tuple
        for idx, part in enumerate(num):
            if type(part) == tuple:
                sub_pos = find_leftmost_pair_nested_multiple_times(part, threshold, depth + 1)
                if sub_pos is not None:
                    sub_pos.insert(0, idx)
                    return sub_pos
    else:
        if depth > threshold:
            return []
    return None


def find_position_of_big_num(num: SnailFishNumber, threshold: int = 10) -> (Position, int):
    """return the position of the leftmost number bigger than threshold"""

    for idx, part in enumerate(num):
        if type(part) == int:
            if part >= threshold:
                return [idx], part
        else:
            sub_pos, num = find_position_of_big_num(part, threshold)
            if sub_pos is not None:
                sub_pos.insert(0, idx)
                return sub_pos, num
    return None, 0


def reduce_number(a: SnailFishNumber) -> SnailFishNumber:
    """reduce a snail-fish number according to the rules"""
    curr_number = deepcopy(a)
    while True:
        """
        repeatedly first one that applies
        - If any pair is nested inside four pairs, the leftmost such pair explodes.
        - If any regular number is 10 or greater, the leftmost such regular number splits.
        """
        # first rule
        explode_pos = find_leftmost_pair_nested_multiple_times(curr_number)
        if explode_pos is not None:
            exploding_pair = get_sfn(curr_number, explode_pos)
            left_pos = find_first_left_number(curr_number, explode_pos)
            if left_pos is not None:  # if exists, add left value to first left
                curr_number = set_sfn(curr_number, left_pos, get_sfn(curr_number, left_pos) + exploding_pair[0])
            right_pos = find_first_right_number(curr_number, explode_pos)
            if right_pos is not None:  # if exists, add right value to first right
                curr_number = set_sfn(curr_number, right_pos, get_sfn(curr_number, right_pos) + exploding_pair[1])
            # replace exploding pair with 0
            curr_number = set_sfn(curr_number, explode_pos, 0)
            continue
            # if first rule applied, second rule is skipped
        # second rule
        split_pos, split_num = find_position_of_big_num(curr_number)
        if split_pos is not None:
            new_tup: SnailFishNumber = (int(split_num / 2), split_num - int(split_num / 2))
            curr_number = set_sfn(curr_number, split_pos, new_tup)
            continue
        # if no rule matched, number is reduced
        return curr_number


def add_numbers(a: SnailFishNumber, b: SnailFishNumber) -> SnailFishNumber:
    """add two snail-fish number"""
    # concat numbers (addition)
    new_number: SnailFishNumber = (a, b)
    # reduce number and return
    return reduce_number(new_number)


def add_list_of_numbers(list_of_nums: List[SnailFishNumber]) -> SnailFishNumber:
    """add all numbers in a list pairwise on top of each other"""
    curr_num = list_of_nums[0]
    for i in range(1, len(list_of_nums)):
        curr_num = add_numbers(curr_num, list_of_nums[i])
    return curr_num


def largest_magnitude_of_two_snf_nums(list_of_nums: List[SnailFishNumber]) -> int:
    """largest magnitude gotten by adding two SNF numbers of a list of SNF"""
    magnitudes = []
    for i in range(len(list_of_nums)):
        for j in range(len(list_of_nums)):
            mag = calculate_magnitude(add_numbers(deepcopy(list_of_nums[i]), deepcopy(list_of_nums[j])))
            magnitudes.append(mag)
    return max(magnitudes)


def calculate_magnitude(num: tuple) -> int:
    """calculate the magnitude of a given number"""
    if type(num[0]) is int:
        part1 = num[0]
    else:
        part1 = calculate_magnitude(num[0])
    if type(num[1]) is int:
        part2 = num[1]
    else:
        part2 = calculate_magnitude(num[1])
    return 3 * part1 + 2 * part2


class Test2021Day18(unittest.TestCase):
    homework_assignment = [
        (((0, (5, 8)), ((1, 7), (9, 6))), ((4, (1, 2)), ((1, 4), 2))),
        (((5, (2, 8)), 4), (5, ((9, 9), 0))),
        (6, (((6, 2), (5, 6)), ((7, 6), (4, 7)))),
        (((6, (0, 7)), (0, 9)), (4, (9, (9, 0)))),
        (((7, (6, 4)), (3, (1, 3))), (((5, 5), 1), 9)),
        ((6, ((7, 3), (3, 2))), (((3, 8), (5, 7)), 4)),
        ((((5, 4), (7, 7)), 8), ((8, 3), 8)),
        ((9, 3), ((9, 9), (6, (4, 9)))),
        ((2, ((7, 7), 7)), ((5, 8), ((9, 3), (0, 2)))),
        ((((5, 2), 5), (8, (3, 7))), ((5, (7, 5)), (4, 4)))
    ]

    larger_example = [
        (((0, (4, 5)), (0, 0)), (((4, 5), (2, 6)), (9, 5))),
        (7, (((3, 7), (4, 3)), ((6, 3), (8, 8)))),
        ((2, ((0, 8), (3, 4))), (((6, 7), 1), (7, (1, 6)))),
        ((((2, 4), 7), (6, (0, 5))), (((6, 8), (2, 8)), ((2, 1), (4, 5)))),
        (7, (5, ((3, 8), (1, 4)))),
        ((2, (2, 2)), (8, (8, 1))),
        (2, 9),
        (1, (((9, 3), 9), ((9, 0), (0, 7)))),
        (((5, (7, 4)), 7), 1),
        ((((4, 2), 2), 6), (8, 7))
    ]

    larger_example_results = [
        ((((4, 0), (5, 4)), ((7, 7), (6, 0))), ((8, (7, 7)), ((7, 9), (5, 0)))),
        ((((6, 7), (6, 7)), ((7, 7), (0, 7))), (((8, 7), (7, 7)), ((8, 8), (8, 0)))),
        ((((7, 0), (7, 7)), ((7, 7), (7, 8))), (((7, 7), (8, 8)), ((7, 7), (8, 7)))),
        ((((7, 7), (7, 8)), ((9, 5), (8, 7))), (((6, 8), (0, 8)), ((9, 9), (9, 0)))),
        ((((6, 6), (6, 6)), ((6, 0), (6, 7))), (((7, 7), (8, 9)), (8, (8, 1)))),
        ((((6, 6), (7, 7)), ((0, 7), (7, 7))), (((5, 5), (5, 6)), 9)),
        ((((7, 8), (6, 7)), ((6, 8), (0, 8))), (((7, 7), (5, 0)), ((5, 5), (5, 6)))),
        ((((7, 7), (7, 7)), ((8, 7), (8, 7))), (((7, 0), (7, 7)), 9)),
        ((((8, 7), (7, 7)), ((8, 6), (7, 7))), (((0, 7), (6, 6)), (8, 7)))
    ]

    def test_addition(self):
        a: SnailFishNumber = ((((4, 3), 4), 4), (7, ((8, 4), 9)))
        b: SnailFishNumber = (1, 1)
        self.assertEqual(add_numbers(a, b), ((((0, 7), 4), ((7, 8), (6, 0))), (8, 1)))

    def test_addition_v2(self):
        a: SnailFishNumber = (((0, (4, 5)), (0, 0)), (((4, 5), (2, 6)), (9, 5)))
        b: SnailFishNumber = (7, (((3, 7), (4, 3)), ((6, 3), (8, 8))))
        self.assertEqual(add_numbers(a, b), ((((4, 0), (5, 4)), ((7, 7), (6, 0))), ((8, (7, 7)), ((7, 9), (5, 0)))))

    def test_find_left(self):
        for num, pos, new_pos in [
            [(((((9, 8), 1), 2), 3), 4), [0, 0, 0, 0, 0], None],
            [(((((9, 8), 1), 2), 3), 4), [1], [0, 1]],
            [(((((9, 8), 1), 2), 3), 4), [0, 1], [0, 0, 1]],
            [(4, ((((9, 8), 1), 2), 3)), [1, 0, 0, 0, 0], [0]],
            [(4, (1, 2)), [1, 0], [0]],
            [(4, (1, 2)), [1], [0]],
            [(4, (1, (3, 5))), [1, 1, 0], [1, 0]],
            [(((((9, 8), 1), 2), 3), 4), [0, 0, 0, 0], None],
            [[0, [[[4, 5], [2, 6]], [9, 5]]], [1, 1, 0], [1, 0, 1, 1]],
        ]:
            with self.subTest():
                self.assertEqual(find_first_left_number(num, pos), new_pos)

    def test_find_right(self):
        for num, pos, new_pos in [
            [(((((9, 8), 1), 2), 3), 4), [0, 0, 0, 0, 0], [0, 0, 0, 0, 1]],
            [(4, ((((9, 8), 1), 2), 3)), [0], [1, 0, 0, 0, 0]],
            [(4, ((((9, 8), 1), 2), 3)), [1, 1], None],
            [(4, ((((9, 8), 1), 2), (5, 6))), [1, 0, 1], [1, 1, 0]],
            [(4, (1, (3, 5))), [1, 1, 1], None],
            [(4, (1, (3, 5))), [1, 1, 0], [1, 1, 1]],
            [(4, (1, (3, 5))), [1, 1], None],
            [(4, (1, (3, 5))), [1, 0], [1, 1, 0]],
            [(4, ((2, 7), (3, 5))), [1, 0], [1, 1, 0]],
            [((6, (5, (7, (3, 2)))), 1), [0, 1, 1, 1], [1]],
            [[0, [[[4, 5], [2, 6]], [9, 5]]], [1, 0, 1, 1], [1, 1, 0]],
        ]:
            with self.subTest():
                self.assertEqual(find_first_right_number(num, pos), new_pos)

    def test_explode(self):
        for num, new_num in [
            [(((((9, 8), 1), 2), 3), 4), ((((0, 9), 2), 3), 4)],
            [(7, (6, (5, (4, (3, 2))))), (7, (6, (5, (7, 0))))],
            [((6, (5, (4, (3, 2)))), 1), ((6, (5, (7, 0))), 3)],
            [((3, (2, (8, 0))), (9, (5, (4, (3, 2))))), ((3, (2, (8, 0))), (9, (5, (7, 0))))],
            [(((((1, (2, 3)), 4), 5), 6), 7), ((((0, 7), 5), 6), 7)],
            [((((((5, 6), (2, 3)), 4), 5), 6), 7), ((((0, 7), 5), 6), 7)],
        ]:
            with self.subTest():
                self.assertEqual(reduce_number(num), reduce_number(new_num))

    def test_get(self):
        for sfn, path, res in [
            [((7, 8), 1), [0, 0], 7],
            [((7, 8), 1), [0, 1], 8],
            [(1, ((4, 7), 8)), [1, 0, 1], 7],
            [(1, ((8, 8), 2)), [0], 1],
            [(1, ((8, 8), 2)), [1], ((8, 8), 2)],
        ]:
            with self.subTest():
                self.assertEqual(get_sfn(sfn, path), res)

    def test_set_final(self):
        for sfn, path, new_num, new_sfn in [
            [(7, 8), [1], 9, (7, 9)],
            [(7, 8), [1], (1, 2), (7, (1, 2))],
            [((7, 8), 1), [1], 9, ((7, 8), 9)],
            [((7, 8), 1), [0, 1], (0, 2), ((7, (0, 2)), 1)],
            [((7, 8), 1), [0, 1], (0, (2, 3)), ((7, (0, (2, 3))), 1)],
            [(1, (8, 8)), [1, 1], (2, 3), (1, (8, (2, 3)))],
            [(1, ((8, 8), 2)), [1, 0, 1], (3, 3), (1, ((8, (3, 3)), 2))],
        ]:
            with self.subTest():
                self.assertEqual(set_sfn(sfn, path, new_num), new_sfn)

    def test_set_non_leaf(self):
        for sfn, path, new_num, new_sfn in [
            [((7, 8), 1), [0], 9, (9, 1)],
            [(1, (8, 8)), [1], (2, 3), (1, (2, 3))],
            [((1, 1), ((8, 8), 2)), [1], (1, 1), ((1, 1), (1, 1))],
        ]:
            with self.subTest():
                self.assertEqual(set_sfn(sfn, path, new_num), new_sfn)

    def test_magnitude(self):
        for number, magn in [
            [((1, 2), ((3, 4), 5)), 143],
            [((((0, 7), 4), ((7, 8), (6, 0))), (8, 1)), 1384],
            [((((1, 1), (2, 2)), (3, 3)), (4, 4)), 445],
            [((((3, 0), (5, 3)), (4, 4)), (5, 5)), 791],
            [((((5, 0), (7, 4)), (5, 5)), (6, 6)), 1137],
            [((((8, 7), (7, 7)), ((8, 6), (7, 7))), (((0, 7), (6, 6)), (8, 7))), 3488],
            [((((6, 6), (7, 6)), ((7, 7), (7, 0))), (((7, 7), (7, 7)), ((7, 8), (9, 9)))), 4140],
        ]:
            with self.subTest():
                self.assertEqual(calculate_magnitude(number), magn)

    def test_sum_of_list_of_nums(self):
        for nums, res_num in [
            [[(1, 1), (2, 2), (3, 3), (4, 4)], ((((1, 1), (2, 2)), (3, 3)), (4, 4))],
            [[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], ((((3, 0), (5, 3)), (4, 4)), (5, 5))],
            [[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], ((((5, 0), (7, 4)), (5, 5)), (6, 6))],
            [deepcopy(self.homework_assignment),
             ((((6, 6), (7, 6)), ((7, 7), (7, 0))), (((7, 7), (7, 7)), ((7, 8), (9, 9))))],
        ]:
            with self.subTest():
                self.assertEqual(add_list_of_numbers(nums), res_num)

    def test_sum_of_list_of_nums_larger_example_stepwise(self):
        for i in range(2, len(self.larger_example)):
            curr_res = add_list_of_numbers(self.larger_example[:i])
            self.assertEqual(curr_res, self.larger_example_results[i - 2])

    def test_split(self):
        for num, new_num in [
            [(15, 1), ((7, 8), 1)],
            [(1, 16), (1, (8, 8))],
            [(1, (16, 2)), (1, ((8, 8), 2))],
            [((16, 2), 1), (((8, 8), 2), 1)],
        ]:
            with self.subTest():
                self.assertEqual(reduce_number(num), reduce_number(new_num))

    def test_largest_magnitude_for_pair(self):
        self.assertEqual(largest_magnitude_of_two_snf_nums(self.homework_assignment), 3993)


if __name__ == '__main__':
    def str_to_snail_fish_number(string: str) -> SnailFishNumber:
        """convert a string of list of lists to a SFN"""
        try:
            s = eval(string)
            if type(s) == tuple:
                return s
        except:
            raise Exception("Snail-fish number can not be converted")

    print(">>> Start Main 18:")
    puzzle_input = read_lines_as_list("data/18.txt")
    puzzle_tuples = []
    for line in puzzle_input:
        line: str
        line = line.replace("[", "(")
        line = line.replace("]", ")")
        puzzle_tuples.append(str_to_snail_fish_number(line))
    print("Part 1): ", calculate_magnitude(add_list_of_numbers(deepcopy(puzzle_tuples))))
    print("Part 2): ", largest_magnitude_of_two_snf_nums(deepcopy(puzzle_tuples)))
    print("End Main 18<<<")
