import unittest
from typing import Dict, List, Tuple, Set

from helper.file import read_lines_as_list

Mapping_t = Dict[str, str]

activated_segments: Dict[int, Set[str]] = {
    0: {"a", "b", "c", "e", "f", "g"},
    1: {"c", "f"},
    2: {"a", "c", "d", "e", "g"},
    3: {"a", "c", "d", "f", "g"},
    4: {"b", "c", "d", "f"},
    5: {"a", "b", "d", "f", "g"},
    6: {"a", "b", "d", "e", "f", "g"},
    7: {"a", "c", "f"},
    8: {"a", "b", "c", "d", "e", "f", "g"},
    9: {"a", "b", "c", "d", "e", "f", "g"},
}

# length: shown number
poss_values: Dict[int, List[int]] = {
    2: [1],
    3: [7],
    4: [4],
    5: [2, 3, 5],
    6: [0, 6],
    7: [8],
}

active_subsets: Dict[int, Set[int]] = {
    0: {1, 7},
    3: {1, 7},
    4: {1},
    6: {5},
    7: {1},
    9: {3, 4}
}


def merge_numbers(nums: List[int]) -> int:
    """given a list of int, merge them together"""
    return int("".join(str(num) for num in nums))


def map_unique_len_to_num(length: int) -> int:
    """for a given set of chars, return its corresponding number"""
    if length in poss_values and len(poss_values[length]) == 1:
        return poss_values[length][0]
    else:
        raise Exception("length {} is not unique".format(length))


def map_str_list_to_int(mapping: Dict[int, Set[str]], output: List[str]) -> int:
    """For a given mapping, convert output to number"""
    vals = []
    for out_str in output:
        for num, seq in mapping.items():
            if seq == set(out_str):
                vals.append(num)
    return merge_numbers(vals)


def find_unique(output: List[str]) -> List[bool]:
    """find unique numbers in output"""
    return [len(poss_values[len(word)]) == 1 for word in output]


def find_mapping_for_lhs(inp: List[str]) -> Dict[int, Set[str]]:
    """for each string, deduce what numbers are represented"""
    char_map: Dict[int, Set[str]] = {}
    # set length unique numbers to their respective value
    lhs_unique = find_unique(inp)
    for i, unique in enumerate(lhs_unique):
        if unique:
            unique_str = inp[i]
            unique_chars = set(unique_str)
            unique_num = map_unique_len_to_num(len(unique_str))
            char_map[unique_num] = unique_chars

    # every number has to be in input just once
    # [0, 6, 9] -> length 6
    six_digit = [set(val) for val in inp if len(val) == 6]
    for val in six_digit:
        if not char_map[1].issubset(val):  # 6 iff not subset 1
            char_map[6] = val
        elif char_map[4].issubset(val):  # 9 if 4 is subset
            char_map[9] = val
        else:  # else 0
            char_map[0] = val
    # [2, 3, 5] -> length 5
    five_digit = [set(val) for val in inp if len(val) == 5]
    for val in five_digit:
        if char_map[1].issubset(val):  # only 3 has subset 1
            char_map[3] = val
            continue
        # set(5) - set(9) has to be empty
        val_ = val.copy()
        for i3 in char_map[9]:
            if i3 in val:
                val_.remove(i3)
        if len(val_) == 0:
            char_map[5] = val
        else:
            char_map[2] = val

    return char_map


def load_data(filepath: str) -> (List[str], List[str]):
    """load data from file"""
    data_input = read_lines_as_list(filepath, split=" | ")
    data_input_lhs = [line[0] for line in data_input]
    data_input_output = [line[1] for line in data_input]
    data_input_lhs_ = [line.split(" ") for line in data_input_lhs]
    data_input_output_ = [line.split(" ") for line in data_input_output]
    return data_input_lhs_, data_input_output_


def map_line(lhs: List[str], rhs: List[str]) -> int:
    """given the lhs and rhs of the data, get the numbers of the rhs"""
    # check if rhs is solved by unique numbers
    if all(find_unique(rhs)):  # all unique
        rhs_sol = [map_unique_len_to_num(len(val)) for val in rhs]
        return merge_numbers(rhs_sol)
    else:  # analyze lhs
        line_mapping = find_mapping_for_lhs(lhs)
        return map_str_list_to_int(line_mapping, rhs)


class Test2021Day08(unittest.TestCase):
    def test_find_unique(self):
        for outp, res in [
            [["fdgacbe", "cefdb", "cefbgd", "gcbe"], [True, False, False, True]],
            [["fcgedb", "cgb", "dgebacf", "gc"], [False, True, True, True]]
        ]:
            with self.subTest():
                self.assertListEqual(find_unique(outp), res)

    def check_first_test_line(self):
        test_lhs, test_rhs = load_data("data/08-test.txt")
        lhs = test_lhs[0], rhs = test_rhs[0]
        number_mapping = find_mapping_for_lhs(lhs)
        sol = {
            8: "acedgfb",
            5: "cdfbe",
            2: "gcdfa",
            3: "fbcad",
            7: "dab",
            9: "cefabd",
            6: "cdfgeb",
            4: "eafb",
            0: "cagedb",
            1: "ab",
        }
        self.assertDictEqual(number_mapping, sol)
        self.assertEqual(map_line(lhs, rhs), 5353)

    def test_solve_example(self):
        test_lhs, test_rhs = load_data("data/08-test.txt")
        numbers = [map_line(lhs=test_lhs[i], rhs=test_rhs[i]) for i in range(len(test_lhs))]
        self.assertEqual(numbers[0], 8394)
        self.assertEqual(sum(numbers), 61229)


if __name__ == '__main__':
    print(">>> Start Main 08:")
    puzzle_lhs, puzzle_output = load_data("data/08.txt")
    print("Part 1): ", sum(sum(find_unique(out)) for out in puzzle_output))
    print("Part 2): ", sum(map_line(lhs=puzzle_lhs[i], rhs=puzzle_output[i]) for i in range(len(puzzle_lhs))))
    print("End Main 08<<<")
