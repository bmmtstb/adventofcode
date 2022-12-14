import unittest
from typing import Dict, List

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
    if len(s1) != len(s2):
        raise Exception(f'Strings should have same length. [{s1}] [{s2}]')
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
    def test_char_multiples(self):
        for s, d in [
            ["abcdef", {"a": 1, "b": 1}],
            ["aabcdd", {"a": 2, "d": 2}],
            ["abcdee", {"e": 2}],
            ["ababab", {"a": 3, "b": 3}],
        ]:
            with self.subTest():
                m = get_letter_multiples(s)
                for key, value in d.items():
                    self.assertTrue(key in m)
                    self.assertEqual(value, m[key])

    def test_checksum(self):
        list_ = ["abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab"]
        self.assertEqual(calculate_checksum(list_), 12)

    def test_difference(self):
        for s1, s2, b in [
            ["abcde", "axcye", False],
            ["fghij", "fguij", True],
        ]:
            with self.subTest():
                self.assertEqual(check_difference(s1, s2), b)

    def test_find_closing_matching_string(self):
        l = ["abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz"]
        t = ("fghij", "fguij")
        self.assertTupleEqual(find_closely_matching_strings(l), t)


if __name__ == '__main__':
    print(">>> Start Main 02:")
    puzzle_input = read_lines_as_list("data/02.txt")
    print("Part 1): ", calculate_checksum(puzzle_input))
    print("Part 2): ", find_closely_matching_strings(puzzle_input))
    print("End Main 02<<<")
