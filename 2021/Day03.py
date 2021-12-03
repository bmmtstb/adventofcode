import unittest
from parameterized import parameterized
from typing import Dict, List, Tuple, Set, Union

from helper.file import read_lines_as_list


def get_word_row_counts(data: List[str]) -> List[Dict[int, int]]:
    """Given a list of Strings, count the appearance per index of each character"""
    res = []
    for i in range(len(data[0])):
        cc = get_char_row_count(data, i)
        res.append(cc)
    return res


def get_char_row_count(data: List[str], idx: int) -> Dict[int, int]:
    """given a list of strings, count the characters at index of every word and return the char frequency"""
    char_count: Dict[int, int] = {}
    for word in data:
        if int(word[idx]) in char_count:
            char_count[int(word[idx])] += 1
        else:
            char_count[int(word[idx])] = 1
    return char_count



def get_row_common(row_counts: List[Dict[int, int]], f: Union[min, max]) -> str:
    """Given the row counts of each char, return the most or least common per row"""
    res = ""
    for count in row_counts:
        res += str(f(count, key=count.get))
    return res


def filter_data(d: List[str], criterion: str) -> str:
    """given a list of strings, filter them according to the given rules"""
    """
    RULES
    - Keep only numbers selected by the bit criteria for the type of rating value for which you are searching. Discard numbers which do not match the bit criteria.
    - If you only have one number left, stop; this is the rating value for which you are searching.
    - Otherwise, repeat the process, considering the next bit to the right.
    
    BIT CRITERIA:    
    To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 1 in the position being considered.
    To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 0 in the position being considered.
    """
    if criterion not in ["CO2", "O2GEN"]:
        raise Exception("Invalid criterion {}".format(criterion))

    resulting_data = d.copy()
    for i in range(len(d[0])):
        idx_counts = get_char_row_count(resulting_data, i)
        # check if values exist
        if 0 not in idx_counts:
            common = 1
        elif 1 not in idx_counts:
            common = 0
        # both values exist
        elif criterion == "CO2":
            common = 0 if idx_counts[0] <= idx_counts[1] else 1
        else:
            common = 1 if idx_counts[1] >= idx_counts[0] else 0
        # common is known
        resulting_data = [word for word in resulting_data if word[i] == str(common)]
        if len(resulting_data) == 1:
            return resulting_data[0]
    raise Exception("No solution found.")


class Test2021Day03(unittest.TestCase):
    default_data_short = ["00", "11", "10", "10", "10", "01", "00", "11", "10", "11", "00", "01"]
    default_data = ["00100", "11110", "10110", "10111", "10101", "01111", "00111", "11100", "10000", "11001", "00010", "01010"]

    def test_row_counts(self):
        self.assertEqual(get_word_row_counts(self.default_data_short.copy()), [{0: 5, 1: 7}, {0: 7, 1: 5}])

    @parameterized.expand([
        [max, "10110"],
        [min, "01001"],
    ])
    def test_common(self, f, r):
        c = get_word_row_counts(self.default_data.copy())
        self.assertEqual(get_row_common(c, f), r)

    @parameterized.expand([
        ["O2GEN", "10111"],
        ["CO2", "01010"],
    ])
    def test_filter_data(self, crit, res):
        self.assertEqual(filter_data(self.default_data.copy(), crit), res)


if __name__ == '__main__':
    print(">>> Start Main 03:")
    puzzle_input = read_lines_as_list("data/03.txt")
    counts = get_word_row_counts(puzzle_input.copy())
    gamma_bin = get_row_common(counts, min)
    eps_bin = get_row_common(counts, max)
    print("Part 1): ")
    print("Gamma: ", gamma_bin, " -> ", int(gamma_bin, 2))
    print("Eps: ", eps_bin, " -> ", int(eps_bin, 2))
    print("--> ", int(gamma_bin, 2) * int(eps_bin, 2))
    print("Part 2): ")
    O2GEN_bin = filter_data(puzzle_input.copy(), "O2GEN")
    CO2_bin = filter_data(puzzle_input.copy(), "CO2")
    print("O2GEN: ", O2GEN_bin, " -> ", int(O2GEN_bin, 2))
    print("CO2: ", CO2_bin, " -> ", int(CO2_bin, 2))
    print("--> ", int(CO2_bin, 2) * int(O2GEN_bin, 2))
    print("End Main 03<<<")
