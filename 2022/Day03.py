import unittest
from typing import Dict, List, Tuple, Set

from helper.file import read_lines_as_list


def split_rucksack(rucksack: str) -> List[str]:
    """given a string split it in half"""
    middle = len(rucksack) // 2
    return [rucksack[:middle], rucksack[middle:]]


def get_character_priority(char: str) -> int:
    """get the character priority of a given character"""
    return ord(char) - ord("a") + 1 if char.islower() else ord(char) - ord("A") + 27


def get_sharing_priority(rucksack: List[str]) -> int:
    """find duplicate character and return its priority"""
    l, r = rucksack
    char: str = set(l).intersection(set(r)).pop()
    return get_character_priority(char)


def get_rucksack_priority_score(rucksacks: List[str]) -> int:
    """get the sum of all the in rucksack sharing priority items"""
    return sum(get_sharing_priority(split_rucksack(rucksack)) for rucksack in rucksacks)


def get_group_item_priority(rucksacks: List[str]) -> int:
    """given a group of three rucksacks, get the common item, return its priority"""
    a, b, c = rucksacks
    char: str = set(a).intersection(set(b)).intersection(set(c)).pop()
    return get_character_priority(char)


def get_group_priority_scores(rucksacks: List[str]) -> int:
    """get the sum of all group priority items"""
    # step every third and use list slicing to combine the lists
    return sum(get_group_item_priority(rucksacks[start_idx:start_idx+3]) for start_idx in range(0, len(rucksacks), 3))


class Test2022Day03(unittest.TestCase):
    test_rucksacks = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]

    def test_split_rucksack(self):
        self.assertEqual(split_rucksack("vJrwpWtwJgWrhcsFMMfFFhFp"), ["vJrwpWtwJgWr", "hcsFMMfFFhFp"])

    def test_get_sharing_priority(self):
        for idx, priority in [
            (0, 16),
            (1, 38),
            (2, 42),
            (3, 22),
            (4, 20),
            (5, 19),
        ]:
            with self.subTest(msg=f'Rucksack: {self.test_rucksacks[idx]}'):
                self.assertEqual(get_sharing_priority(split_rucksack(self.test_rucksacks[idx])), priority)

    def test_get_rucksack_priority_score(self):
        self.assertEqual(get_rucksack_priority_score(self.test_rucksacks), 157)

    def test_get_group_item_priority(self):
        group = ["vJrwpWtwJgWrhcsFMMfFFhFp","jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL","PmmdzqPrVvPwwTWBwg"]
        self.assertEqual(get_group_item_priority(group), 18)

    def test_get_group_priority_scores(self):
        self.assertEqual(get_group_priority_scores(self.test_rucksacks), 70)


if __name__ == '__main__':
    print(">>> Start Main 03:")
    puzzle_input = read_lines_as_list(filepath="data/03.txt")
    print("Part 1): ", get_rucksack_priority_score(puzzle_input))
    print("Part 2): ", get_group_priority_scores(puzzle_input))
    print("End Main 03<<<")
