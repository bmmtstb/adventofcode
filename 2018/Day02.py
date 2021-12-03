import unittest
from parameterized import parameterized
from typing import Dict, List, Tuple, Set

from helper.file import read_lines_as_list


def get_letter_multiples(s: str) -> Dict[str, int]:
    """count how often each letter is present in a string"""
    d: dict = {}
    for char in s:
        if char in d.keys():
            d[char] += 1
        else:
            d[char] = 1
    return d


def calculate_checksum(l: List[str]) -> int:
    """calculate nof strings where a letter appears exactly twice
        multiplied by nof strings where a char appears exactly three times"""
    twice = 0
    trice = 0
    for word in l:
        d = get_letter_multiples(word)
        twice += 1 if 2 in d.values() else 0
        trice += 1 if 3 in d.values() else 0
    return twice * trice


def check_difference(s1: str, s2: str) -> int:
    """given two strings return if the number of uncommon characters is not bigger than one"""
    assert len(s1) == len(s2)
    diff = 0
    for i in range(len(s1)):
        diff += 0 if s1[i] == s2[i] else 1
        if diff > 1:
            return False
    return True


def find_closely_matching_strings(l: List[str]) -> (str, str):
    """in a list of strings, find two strings that match but differ by one character"""
    for s1_idx in range(len(l)):
        for s2_idx in range(s1_idx + 1, len(l)):
            if check_difference(l[s1_idx], l[s2_idx]):
                return l[s1_idx], l[s2_idx]
    return None


class Test2021Day02(unittest.TestCase):
    @parameterized.expand([
        ["abcdef", {"a": 1, "b": 1}],
        ["aabcdd", {"a": 2, "d": 2}],
        ["abcdee", {"e": 2}],
        ["ababab", {"a": 3, "b": 3}],
    ])
    def test_char_multiples(self, s, d):
        self.assertDictContainsSubset(d, get_letter_multiples(s))

    @parameterized.expand([
        [["abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab"], 12],
    ])
    def test_checksum(self, l, check):
        self.assertEqual(calculate_checksum(l), check)

    @parameterized.expand([
        ["abcde", "axcye", False],
        ["fghij", "fguij", True],
    ])
    def test_difference(self, s1, s2, b):
        self.assertEqual(check_difference(s1, s2), b)

    @parameterized.expand([
        [["abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz"], ("fghij", "fguij")],
    ])
    def test_difference(self, l, t):
        self.assertTupleEqual(find_closely_matching_strings(l), t)


if __name__ == '__main__':
    print(">>> Start Main 02:")
    puzzle_input = read_lines_as_list("data/02.txt")
    print("Part 1): ", calculate_checksum(puzzle_input))
    print("Part 2): ", find_closely_matching_strings(puzzle_input))
    print("End Main 02<<<")
