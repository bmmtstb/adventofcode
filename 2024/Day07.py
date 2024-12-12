import unittest

from helper.file import read_lines_as_list


def load_data(fp: str) -> list[tuple[int, list[int]]]:
    """Load the results and the individual numbers from a file."""
    lines = read_lines_as_list(fp, split=": ")
    return [(int(line[0]), list(map(int, line[1].split(" ")))) for line in lines]


def can_equation_be_solved(
    equation: list[int], result: int, operators: list[str] = None, value: int = None
) -> bool:
    """Check if the equation can be solved to the result using the given operators in a left to right fashion."""
    if operators is None:
        operators = ["+", "*"]

    if value is None:
        value = equation[0]
        equation = equation[1:]

    if len(equation) == 0:
        return value == result

    for operator in operators:
        if operator == "+":
            new_value = value + equation[0]
        elif operator == "*":
            new_value = value * equation[0]
        elif operator == "||":
            new_value = int(str(value) + str(equation[0]))
        elif operator == "-":
            new_value = value - equation[0]
        elif operator == "/":
            new_value = value / equation[0]
        else:
            raise ValueError("Operator not supported.")

        if can_equation_be_solved(
            equation=equation[1:], result=result, operators=operators, value=new_value
        ):
            return True

    return False


def part1(lines: list[tuple[int, list[int]]]) -> int:
    """Part1: Check whether the equation can be solved to the result and sum the result of all valid equations."""
    return sum(
        result for result, equation in lines if can_equation_be_solved(equation, result)
    )


def part2(lines: list[tuple[int, list[int]]]) -> int:
    """Part2: Check whether the equation can be solved to the result and sum the result of all valid equations."""
    return sum(
        result
        for result, equation in lines
        if can_equation_be_solved(equation, result, operators=["+", "*", "||"])
    )


class Test2024Day07(unittest.TestCase):

    fp = "./data/07-test.txt"
    test_data = load_data(fp)

    def test_can_equation_be_solved_p1(self):
        for i, solvable in enumerate(
            [True, True, False, False, False, False, False, False, True]
        ):
            with self.subTest(msg="solvable: {}".format(solvable)):
                res, eq = self.test_data[i]
                self.assertEqual(
                    can_equation_be_solved(equation=eq, result=res), solvable
                )

    def test_can_equation_be_solved_p2(self):
        for i, solvable in enumerate(
            [True, True, False, True, True, False, True, False, True]
        ):
            with self.subTest(msg="solvable: {}".format(solvable)):
                res, eq = self.test_data[i]
                self.assertEqual(
                    can_equation_be_solved(
                        equation=eq, result=res, operators=["+", "*", "||"]
                    ),
                    solvable,
                )

    def test_p1(self):
        self.assertEqual(part1(self.test_data), 3749)

    def test_p2(self):
        self.assertEqual(part2(self.test_data), 11387)


if __name__ == "__main__":
    print(">>> Start Main 07:")
    puzzle_data = load_data("./data/07.txt")
    print("Part 1): ", part1(puzzle_data))
    print("Part 2): ", part2(puzzle_data))
    print("End Main 07<<<")
