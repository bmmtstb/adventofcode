import unittest
from typing import Dict, List, Tuple, Set

from helper.file import load_file_and_split


def perform_pair_insertion(start: str, rules: Dict[str, str], nof_steps: int) -> str:
    """Perform multiple steps of pairwise insertion"""
    curr_str = start
    for n in range(nof_steps):
        new_str = curr_str
        for i in range(len(curr_str) - 2, -1, -1):
            substr = curr_str[i:i+2]
            if substr in rules.keys():
                insert_val = rules[substr]
                new_str = new_str[:i+1] + str(insert_val) + new_str[i+1:]
        curr_str = new_str
    return curr_str


def perform_pair_insertion_faster(start: str, rules: Dict[str, str], nof_steps: int) -> int:
    """Perform multiple steps of pairwise insertion - faster"""
    empty_pairs: Dict[str, int] = {key: 0 for key in rules.keys()}
    # count how often a pair is present
    curr_pair_counts: Dict[str, int] = empty_pairs.copy()
    for i in range(len(start) - 2, -1, -1):
        substr = start[i:i + 2]
        curr_pair_counts[substr] += 1
    for n in range(nof_steps):
        new_pair_counts = empty_pairs.copy()
        # update every pair
        for pair in curr_pair_counts:
            new_val: str = rules[pair]
            new_pair_counts[pair[0] + new_val] += curr_pair_counts[pair]
            new_pair_counts[new_val + pair[1]] += curr_pair_counts[pair]
        curr_pair_counts = new_pair_counts.copy()
    # count -> every second char + the first one in start string (unchanged!)
    return polymerase_pair_score(curr_pair_counts, start[0])



def polymerase_str_score(polymerase: str) -> int:
    """most common char minus least common char"""
    # count elements
    elems: Dict[str, int] = {}
    for char in polymerase:
        if char in elems:
            elems[char] += 1
        else:
            elems[char] = 1
    values = list(elems.values())
    values.sort()
    return values[-1] - values[0]


def polymerase_pair_score(pairs: Dict[str, int], first_char: str) -> int:
    """most common char minus least common char"""
    # count elements
    elems: Dict[str, int] = {first_char: 1}
    for char_pair, count in pairs.items():
        if char_pair[1] in elems.keys():
            elems[char_pair[1]] += count
        else:
            elems[char_pair[1]] = count
    values = list(elems.values())
    values.sort()
    return values[-1] - values[0]


class Test2021Day14(unittest.TestCase):
    polymer_start = "NNCB"
    pair_insertion_rule = {
        "CH": "B", "HH": "N", "CB": "H", "NH": "C", "HB": "C", "HC": "B", "HN": "C", "NN": "C", "BH": "H",
        "NC": "B", "NB": "B", "BN": "B", "BB": "N", "BC": "B", "CC": "N", "CN": "C"
    }

    def test_after_n_steps(self):
        for n, res_str in [
            [1, "NCNBCHB"],
            [2, "NBCCNBBBCBHCB"],
            [3, "NBBBCNCCNBBNBNBBCHBHHBCHB"],
            [4, "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"],
        ]:
            with self.subTest():
                self.assertEqual(perform_pair_insertion(self.polymer_start, self.pair_insertion_rule.copy(), n), res_str)

    def test_polymer_length(self):
        for steps, length in [
            [5, 97],
            [10, 3073],
        ]:
            with self.subTest():
                self.assertEqual(len(perform_pair_insertion(self.polymer_start, self.pair_insertion_rule.copy(), steps)), length)

    def test_score(self):
        for steps, score in [
            [10, 1588],
            [40, 2188189693529],
        ]:
            with self.subTest():
                self.assertEqual(perform_pair_insertion_faster(self.polymer_start, self.pair_insertion_rule.copy(), steps), score)



if __name__ == '__main__':
    print(">>> Start Main 14:")
    puzzle_input = load_file_and_split("data/14.txt", separator="\n\n")
    puzzle_template = str(puzzle_input[0])
    puzzle_rules = {line[:2]: line[-1] for line in puzzle_input[1].split("\n")[:-1]}
    puzzle_polymerase = perform_pair_insertion(puzzle_template, puzzle_rules.copy(), 10)
    print("Part 1): ", polymerase_str_score(puzzle_polymerase))
    puzzle_polymerase_2 = perform_pair_insertion_faster(puzzle_template, puzzle_rules.copy(), 40)
    print("Part 2): ", puzzle_polymerase_2)
    print("End Main 14<<<")
