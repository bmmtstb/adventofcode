import unittest
from copy import deepcopy
from typing import Dict, List, Tuple, Set

from helper.file import load_file_and_split

Stack = List[str]
Stacks = List[Stack]
Order = Tuple[int, int, int]
Orders = List[Order]


def load_data(filepath: str) -> Tuple[Stacks, Orders]:
    """load current configuration and move orders from file"""
    raw_config, raw_orders = load_file_and_split(fp=filepath, sep="\n\n")
    raw_config = raw_config.split("\n")
    raw_orders = raw_orders.split("\n")
    # get config into correct format
    nof_stacks = int(raw_config[-1][-1])  # get hightest row number
    nof_items = len(raw_config) - 1  # exclude numbering row
    init_stacks: Stacks = [[] for _ in range(nof_stacks)]
    for row in range(nof_items):
        for stack in range(nof_stacks):
            # row may be shorter
            if len(raw_config[row]) >= 1 + stack * 4:
                value = raw_config[row][1 + stack * 4]
                # dont insert empty boxes
                if value != " ":
                    init_stacks[stack].insert(0, value)
    # get orders
    # get item number 1,3,5 from the split list -> the numbers
    init_orders: Orders = [
        tuple(map(int, order.split(" ")[1::2])) for order in raw_orders
    ]
    return init_stacks, init_orders


def run_orders(init_config: Stacks, orders: Orders, keep_order: bool = False) -> Stacks:
    """Run a list of given orders, does not change init config"""
    config = deepcopy(init_config)
    for order in orders:
        amount, from_number, to_number = order
        # to and from are 1 indexed !
        if not keep_order:  # part 1
            for a in range(amount):
                config[to_number - 1].append(config[from_number - 1].pop())
        else:  # part 2
            config[to_number - 1] += config[from_number - 1][-amount:]
            del config[from_number - 1][-amount:]
    return config


def get_top_of_stack(stacks: Stacks) -> str:
    """get the characters that are on top of each stack"""
    return "".join(stack[-1] for stack in stacks)


class Test2022Day05(unittest.TestCase):
    test_config, test_orders = load_data("data/05-test.txt")
    test_start_config_validation = [["Z", "N"], ["M", "C", "D"], ["P"]]
    test_end_config_validation_single = [["C"], ["M"], ["P", "D", "N", "Z"]]
    test_end_config_validation_multiple = [["M"], ["C"], ["P", "Z", "N", "D"]]

    def test_load_data(self):
        config, _ = load_data("data/05-test.txt")
        self.assertEqual(config, self.test_start_config_validation)

    def test_run_orders(self):
        self.assertEqual(
            run_orders(self.test_config, self.test_orders),
            self.test_end_config_validation_single,
        )
        self.assertEqual(
            run_orders(self.test_config, self.test_orders, keep_order=True),
            self.test_end_config_validation_multiple,
        )

    def test_get_top_of_stack(self):
        for stacks, word in [
            (self.test_config, "NDP"),
            (run_orders(self.test_config, self.test_orders), "CMZ"),
            (run_orders(self.test_config, self.test_orders, keep_order=True), "MCD"),
        ]:
            with self.subTest(msg=f"Word {word}"):
                self.assertEqual(get_top_of_stack(stacks), word)


if __name__ == "__main__":
    print(">>> Start Main 05:")
    puzzle_stack, puzzle_orders = load_data(filepath="data/05.txt")
    print("Part 1): ", get_top_of_stack(run_orders(puzzle_stack, puzzle_orders)))
    print(
        "Part 2): ",
        get_top_of_stack(run_orders(puzzle_stack, puzzle_orders, keep_order=True)),
    )
    print("End Main 05<<<")
