import unittest
from typing import Callable, Dict, List, Tuple, Set, Union
import operator

from helper.file import read_lines_as_list

OPERATORS: Dict[str, Callable] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}

OPPOSITE_OPERATOR: Dict[Callable, Callable] = {
    operator.add: operator.sub,
    operator.sub: operator.add,
    operator.mul: operator.floordiv,
    operator.floordiv: operator.mul,
}


Monkey = Union[int, Tuple[str, Callable, str]]
Monkeys = Dict[str, Monkey]


def load_data(filepath: str) -> Monkeys:
    """read monkeys from file"""
    lines: List[str] = read_lines_as_list(filepath)
    monkeys: Monkeys = {}
    for line in lines:
        name, operation = line.split(": ")
        if any(key in operation for key in OPERATORS.keys()):
            left, op, right = operation.split(" ")
            monkeys[name] = (left, OPERATORS[op], right)
        else:
            monkeys[name] = int(operation)
    return monkeys


def shouting_number(monkeys: Monkeys, root: str = "root") -> int:
    """get the number root shouts"""
    if type(monkeys[root]) is int:
        return monkeys[root]
    else:
        left, op, right = monkeys[root]
        return op(shouting_number(monkeys, left), shouting_number(monkeys, right))


def is_descendant(monkeys: Monkeys, shouter: str, current: str) -> bool:
    """return whether shouter is a descendant of current"""
    if type(monkeys[current]) is int:
        return current == shouter
    else:
        return any(
            [
                is_descendant(monkeys, shouter, monkeys[current][0]),
                is_descendant(monkeys, shouter, monkeys[current][2]),
            ]
        )


def human_shout(monkeys: Monkeys) -> int:
    """what should humn shout so root has an equality"""
    left, _, right = monkeys["root"]
    # check if human shouted in left branch
    did_human_shout_left = is_descendant(monkeys, shouter="humn", current=left)
    # get result of non-human branch
    result = shouting_number(monkeys, root=right if did_human_shout_left else left)
    # backtrack the branch with human inside
    node = left if did_human_shout_left else right

    while node != "humn":
        # get next step of calculations
        left, op, right = monkeys[node]
        # find on which side human did shout
        did_human_shout_left = is_descendant(monkeys, shouter="humn", current=left)
        # get the result where human did not shout
        sub_result = shouting_number(
            monkeys, root=right if did_human_shout_left else left
        )
        # get the new result using the inverse operation, make sure to keep order intact
        # division and minus are not consistent
        if op == operator.sub and not did_human_shout_left:
            # o = p + q -> q = p - o
            result = sub_result - result
        elif op == operator.floordiv and not did_human_shout_left:
            # s = t/u -> u = t/s
            result = sub_result // result
        else:
            result = OPPOSITE_OPERATOR[op](result, sub_result)
        # set new node name
        node = left if did_human_shout_left else right

    return result


class Test2022Day21(unittest.TestCase):
    test_monkeys: Monkeys = load_data("data/21-test.txt")

    def test_shouting_number(self):
        for name, result in [
            ("root", 152),
            ("dbpl", 5),
            ("cczh", 8),
            ("zczc", 2),
            ("ptdq", 2),
            ("dvpt", 3),
            ("lfqf", 4),
            ("humn", 5),
            ("ljgn", 2),
            ("sjmn", 150),
            ("sllz", 4),
            ("pppw", 2),
            ("lgvd", 4),
            ("drzm", 30),
            ("hmdt", 32),
        ]:
            with self.subTest(msg=f"name: {name}"):
                self.assertEqual(shouting_number(self.test_monkeys, name), result)

    def test_is_descendant(self):
        """test if humn is descendant of shouter"""
        for name, descendant in [
            ("root", True),
            ("dbpl", False),
            ("cczh", True),
            ("zczc", False),
            ("ptdq", True),
            ("dvpt", False),
            ("lfqf", False),
            ("humn", True),
            ("ljgn", False),
            ("sjmn", False),
            ("sllz", False),
            ("pppw", True),
            ("lgvd", True),
            ("drzm", False),
            ("hmdt", False),
        ]:
            with self.subTest(msg=f"name: {name}"):
                self.assertEqual(
                    is_descendant(self.test_monkeys, "humn", name), descendant
                )

    def test_root_number(self):
        self.assertEqual(shouting_number(self.test_monkeys), 152)

    def test_humn_shout(self):
        self.assertEqual(human_shout(self.test_monkeys), 301)

    def test_humn_shout_puzzle(self):
        self.assertEqual(human_shout(load_data("data/21.txt")), 3243420789721)


if __name__ == "__main__":
    print(">>> Start Main 21:")
    puzzle_input: Monkeys = load_data("data/21.txt")
    print("Part 1): ", shouting_number(puzzle_input.copy()))
    # not 7241459543177
    # -> 3243420789721
    print("Part 2): ", human_shout(puzzle_input.copy()))
    print("End Main 21<<<")
