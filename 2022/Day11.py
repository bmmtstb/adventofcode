import unittest
import operator
from copy import deepcopy
from typing import Callable, Dict, List, Tuple, Set, Union

from helper.file import load_file_and_split

OPERATORS = {
    "+": operator.add,
    "-": operator.sub,  # not needed
    "*": operator.mul,
}

PassedItem = Tuple[Union[int, None], Union[int, None]]
PassedItems = List[PassedItem]


class Monkey:
    def __init__(self, monkey_infos: str):
        # set types and default values, will be overridden by load_data
        self.items: List[int] = []
        self.operation: Callable = lambda x: x
        self.divisible_test_factor: int = 0
        self.true_id: int = -1
        self.false_id: int = -1
        # monkey may have another relief factor
        self.relief_factor: int = 3
        # set all data
        self.load_data(monkey_infos)
        # count inspected
        self.nof_inspected_items: int = 0

    def inspect_item(self) -> PassedItem:
        """inspect the first item of items, changes its worry level according to operation"""
        if len(self.items) == 0:
            return None, None

        # inspect first item
        self.nof_inspected_items += 1
        item = self.items.pop(0)

        # perform lambda operation and be relieved that the monkey didn't damage the item
        # this causes your worry level to be divided by three and rounded down to the nearest integer.
        # for part 2 the relief factor changes, and we need to use modulo now
        if self.relief_factor == 3:
            new_number = self.operation(item) // 3
        else:
            new_number = self.operation(item) % self.relief_factor
        # test worry level and return pass Route
        if new_number % self.divisible_test_factor == 0:
            return new_number, self.true_id
        else:
            return new_number, self.false_id

    def inspect_items(self) -> PassedItems:
        """inspect all items of the monkey"""
        passed = []
        while len(self.items) > 0:
            passed.append(self.inspect_item())
        return passed

    def load_data(self, monkey_infos) -> None:
        """load data from file"""
        items, operation, test, true, false = [
            line.split(": ")[1] for line in monkey_infos.split("\n")[1:]
        ]
        # items
        if ", " in items:
            self.items = [int(item) for item in items.split(", ")]
        else:
            self.items = [int(items)]
        # operation
        val1, op, val2 = operation[6:].split(" ")
        self.operation = lambda old: OPERATORS[op](
            old if val1 == "old" else int(val1), old if val2 == "old" else int(val2)
        )
        # test
        self.divisible_test_factor = int(test[13:])
        # true
        self.true_id = int(true[16:])
        # false
        self.false_id = int(false[16:])


class Monkeys:
    def __init__(self, filepath: str):
        self.monkeys: List[Monkey] = [
            Monkey(monkey)
            for monkey in load_file_and_split(filepath=filepath, separator="\n\n")
        ]

    def change_relief_factor(self) -> None:
        """for p2 relief factor is the product of all the monkeys test divisors (all primes)"""
        relief_factor = 1
        for monkey in self.monkeys:
            relief_factor *= monkey.divisible_test_factor
        for monkey in self.monkeys:
            monkey.relief_factor = relief_factor

    def play_round(self) -> None:
        """play a round of 'Keep Away'"""
        for monkey in self.monkeys:
            # inspect all items the monkey has
            passed_items = monkey.inspect_items()
            # send every item from monkey to other monkeys
            for item, target_id in passed_items:
                self.monkeys[target_id].items.append(item)

    def calculate_monkey_business_after_n_rounds(self, n: int = 20) -> int:
        """play the game and get the monkey business score"""
        for _ in range(n):
            self.play_round()
        a, b = sorted([monkey.nof_inspected_items for monkey in self.monkeys])[-2:]
        return a * b


class Test2022Day11(unittest.TestCase):
    test_monkeys: Monkeys = Monkeys("data/11-test.txt")

    def test_play_round(self):
        new_monkeys = deepcopy(self.test_monkeys)
        new_monkeys.play_round()
        self.assertEqual(new_monkeys.monkeys[0].items, [20, 23, 27, 26])
        self.assertEqual(new_monkeys.monkeys[1].items, [2080, 25, 167, 207, 401, 1046])

    def test_after_n_rounds(self):
        self.assertEqual(
            deepcopy(self.test_monkeys).calculate_monkey_business_after_n_rounds(20),
            10605,
        )

    def test_after_large_n_rounds(self):
        monkeys = deepcopy(self.test_monkeys)
        monkeys.change_relief_factor()
        self.assertEqual(
            monkeys.calculate_monkey_business_after_n_rounds(10_000), 2713310158
        )


if __name__ == "__main__":
    print(">>> Start Main 11:")
    puzzle_input = Monkeys("data/11.txt")
    print(
        "Part 1): ", deepcopy(puzzle_input).calculate_monkey_business_after_n_rounds(20)
    )
    puzzle_input.change_relief_factor()
    print("Part 2): ", puzzle_input.calculate_monkey_business_after_n_rounds(10_000))
    print("End Main 11<<<")
