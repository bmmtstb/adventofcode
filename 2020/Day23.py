import unittest
from parameterized import parameterized
from typing import Dict, List, Tuple, Set
from copy import deepcopy


def split_input(data: str) -> List[int]:
    """split the input string"""
    return [int(x) for x in data]


def get_one_and_following(cups: List[int], main: int = 1) -> str:
    """get the neighbors of main in clockwise order"""
    idx = cups.index(main)
    return "".join(str(c) for c in cups[idx + 1:] + cups[:idx])


def get_two_following(cups: List[int], main: int = 1) -> (int, int):
    """get the two following items after main"""
    idx = cups.index(main)
    return cups[(idx + 1) % len(cups)], cups[(idx + 2) % len(cups)]


def perform_n_moves(cups: List[int], n: int = 100) -> List[int]:
    """Play the crabs game for n moves"""
    nof_cups = len(cups)
    curr_i = 0
    # perform moves
    for _ in range(n):
        curr_item = cups[curr_i]
        # pick up the three cups that are immediately clockwise of the current cup.
        curr_removed: List[int]
        if curr_i + 4 > nof_cups:
            tmp = cups + cups
            curr_removed = tmp[curr_i + 1:curr_i + 4]
        else:
            curr_removed = cups[curr_i + 1:curr_i + 4]
        # They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
        curr_selection = [cup for cup in cups if cup not in curr_removed]
        # The crab selects a destination cup: the cup with a label equal to the current cup's label minus one.
        # If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up.
        # If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
        destination_label = cups[curr_i] - 1
        while destination_label not in curr_selection:
            destination_label = destination_label - 1 if destination_label > min(curr_selection) else max(curr_selection)
        destination_id = curr_selection.index(destination_label)
        # The crab places the cups it just picked up so that they are immediately clockwise of the destination cup.
        # They keep the same order as when they were picked up.
        if destination_id + 1 == len(curr_selection):
            curr_selection = curr_selection + curr_removed
        else:
            for rem_id, new_item in enumerate(curr_removed):
                curr_selection.insert(destination_id + rem_id + 1, new_item)
        # The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
        curr_i = (curr_selection.index(curr_item) + 1) % nof_cups
        cups = deepcopy(curr_selection)
    return cups


def perform_n_moves_v2(cups: List[int], n: int = 100) -> List[int]:
    """Faster version - Play the crabs game for n moves"""
    nof_cups = len(cups)
    current = cups[0]
    # get dict from list
    linked_list = {label: cups[(i + 1) % nof_cups] for i, label in enumerate(cups)}
    for _ in range(n):
        # pick up 3 right to current
        last = current
        removed = []
        for i in range(3):
            last = linked_list[last]
            removed.append(last)
        # "remove" the 3 items from current list and relink list
        linked_list[current] = linked_list[last]
        # get destination cup (label - 1 if not in the 3 removed)
        destination = current - 1
        while destination in removed or destination == 0:
            if destination == 0:
                destination = nof_cups
            else:
                destination -= 1
        # put removed cups clockwise of destination and relink list
        linked_list[removed[-1]] = linked_list[destination]
        linked_list[destination] = removed[0]
        # select new current cup
        current = linked_list[current]
    new_cups = [1]
    curr_cup = linked_list[1]
    while curr_cup != 1:
        new_cups.append(curr_cup)
        curr_cup = linked_list[curr_cup]
    return new_cups


class Test2020Day23(unittest.TestCase):
    test_str = "389125467"
    test = split_input(test_str)
    test_million = deepcopy(test) + [i for i in range(len(test) + 1, 1000001)]

    def test_create_million(self):
        self.assertEqual(len(self.test_million), 1000000)

    @parameterized.expand([
        [10, "92658374"],
        [100, "67384529"],
    ])
    def test_n_moves_v1(self, n, result):
        res_order = perform_n_moves(deepcopy(self.test), n)
        self.assertEqual(get_one_and_following(res_order), result)
        if n == 10:
            self.assertTupleEqual(get_two_following(res_order), (9, 2))

    @parameterized.expand([
        [10, "92658374"],
        [100, "67384529"],
    ])
    def test_n_moves_v2(self, n, result):
        res_order = perform_n_moves_v2(deepcopy(self.test), n)
        self.assertEqual(get_one_and_following(res_order), result)
        if n == 10:
            self.assertTupleEqual(get_two_following(res_order), (9, 2))

    def test_ten_million_moves(self):
        n = 10000000
        self.assertTupleEqual(get_two_following(perform_n_moves_v2(deepcopy(self.test_million), n)), (934001, 159792))


if __name__ == '__main__':
    print(">>> Start Main 23:")
    puzzle_input_str = "364297581"
    puzzle_input = split_input(puzzle_input_str)
    print("Part 1):")
    part_1 = perform_n_moves(deepcopy(puzzle_input), 100)
    print(get_one_and_following(part_1))
    print("Part 2):")
    puzzle_million = deepcopy(puzzle_input) + [i for i in range(len(puzzle_input) + 1, 1000001)]
    part_2 = perform_n_moves_v2(puzzle_million, n=10000000)
    x, y = get_two_following(part_2)
    print(x, y)
    print(x * y)
    print("End Main 23<<<")
