import unittest
from typing import Dict, List


def read_file_in_groups(filepath: str) -> List[Dict[str, List[int]]]:
    """reads the file at filepath"""
    groups = []
    with open(filepath) as file:
        current = {}
        person_counter = 0
        for line in file.readlines():
            # end of current group
            if line == "\n":
                groups.append(current)
                current = {}
                person_counter = 0
            # read group
            else:
                for char in line.replace("\n", ""):
                    if char in current.keys():
                        current[char].append(person_counter)
                    else:
                        current[char] = list([person_counter])
                person_counter += 1
        # if theres no newline at the end, append last
        if current.keys():
            groups.append(current)
    return groups


def count_different_questions(groups_data: List[Dict[str, List[int]]]) -> List[int]:
    """given processed data of answered questions, get the count of different questions for each group"""
    unique = []
    for gr in groups_data:
        unique.append(len(gr.keys()))
    return unique


def count_same_in_group(groups_data: List[Dict[str, List[int]]]) -> int:
    """Count how many questions are answered true by all the people in a group"""
    same_in_gr = 0
    for group in groups_data:
        # find number of people in group (highest value of value-list)
        nof_people = max(max(val) for val in group.values())
        for val in group.values():
            if len(val) == nof_people + 1:
                same_in_gr += 1
    return same_in_gr


class Test2020Day06(unittest.TestCase):

    def test_count_different(self):
        self.assertEqual(sum(count_different_questions(read_file_in_groups("data/06-test.txt"))), 11)

    def test_count_same_in_group(self):
        self.assertEqual(count_same_in_group(read_file_in_groups("data/06-test.txt")), 6)


if __name__ == '__main__':
    print(">>> Start Main 06:")
    puzzle_input = read_file_in_groups("data/06.txt")
    print("Part 1):")
    print(sum(count_different_questions(puzzle_input)))
    print("Part 2):")
    print(count_same_in_group(puzzle_input))
    print("End Main 06<<<")
