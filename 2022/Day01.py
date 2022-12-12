import unittest
from typing import Dict, List, Tuple, Set

from helper.file import load_file_and_split


Elf = List[int]
Elves = List[Elf]


def load_data(filepath: str) -> Elves:
    """get a list of items every elf carries"""
    return [[int(calorie) for calorie in elf.strip("\n").split("\n")] for elf in
            load_file_and_split(filepath=filepath, separator="\n\n", instance_type=str)]


def get_elves_with_most_calories(elves: Elves) -> List[Tuple[int, int]]:
    """
    get a descendent list of elves carrying the most calories
    :returns elf_if and amount
    """
    elf_values: List[int] = [sum(elf_values) for elf_values in elves]
    return list(sorted(enumerate(elf_values), key=lambda enum_item: enum_item[1], reverse=True))


def get_three_most_sum(elves: Elves):
    """get sum of calories from the three elves that carrie the most"""
    return sum(elf[1] for elf in get_elves_with_most_calories(elves)[:3])


class Test2022Day01(unittest.TestCase):
    test_data = load_data("data/01-test.txt")

    def test_load_data(self):
        for elf_id, calorie_id, amount in [
            (0, 1, 2000),
            (1, 0, 4000),
            (4, 0, 10000),
        ]:
            with self.subTest(msg=f'Elf {elf_id} carries as item {calorie_id} an amount of {amount}'):
                self.assertEqual(self.test_data[elf_id][calorie_id], amount)

    def test_get_elf_with_most_calories(self):
        for elf_id, pos, amount in [
            (3, 0, 24000),
            (2, 1, 11000),
            (4, 2, 10000),
        ]:
            elves = get_elves_with_most_calories(self.test_data)
            self.assertEqual(elves[pos], (elf_id, amount))

    def test_get_most_three_sum(self):
        self.assertEqual(get_three_most_sum(self.test_data), 45000)


if __name__ == '__main__':
    print(">>> Start Main 01:")
    puzzle_input = load_data("data/01.txt")
    print("Part 1): ", get_elves_with_most_calories(puzzle_input)[0][1])
    print("Part 2): ", get_three_most_sum(puzzle_input))
    print("End Main 01<<<")
