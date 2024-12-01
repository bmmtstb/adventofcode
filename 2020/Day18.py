import unittest
from typing import Dict, List, Tuple, Set, Union


def load_from_file(filepath: str) -> List[str]:
    """load equations from file"""
    with open(filepath) as file:
        d = file.read().split("\n")
    return d


def split_formulars(str_equations: List[str]) -> List[List[Union[str, int]]]:
    """Split Equation into correct types"""
    results = []
    for line in str_equations:
        results.append(
            [c if c in ["+", "*", "(", ")"] else int(c) for c in line if c != " "]
        )
    return results


def solve_l_to_r(equation: List[Union[str, int]], l_to_r: bool = True):
    """Solve an equation from left to right. Parentheses first"""

    def solve_l_to_r_w_o_brackets(eq: List[Union[str, int]]) -> int:
        """solve a simple equation with no parentheses"""
        s = 1
        val = eq[0]
        while s < len(eq):
            if eq[s] == "+":
                val += eq[s + 1]
            elif eq[s] == "*":
                val *= eq[s + 1]
            else:
                raise Exception("unknown operator {}".format(eq[s]))
            s += 2
        return val

    def solve_sum_before_prod_w_o_brackets(eq: List[Union[str, int]]) -> int:
        """solve equation l to r with sums before prods"""
        s = 1
        new_eq = [eq[0]]
        while s < len(eq):
            if eq[s] == "+":
                new_val = new_eq.pop(-1) + eq[s + 1]
                new_eq += [new_val]
            elif eq[s] == "*":
                new_eq += eq[s : s + 2]
            else:
                raise Exception("unknown operator {}".format(eq[s]))
            s += 2
        # there are no more + chars, only multiplications
        return solve_l_to_r_w_o_brackets(new_eq)

    value = 0
    opening_indices = []
    while "(" in equation:
        start = 0 if len(opening_indices) == 0 else opening_indices[-1] + 1
        for i in range(start, len(equation)):
            if equation[i] == "(":
                opening_indices.append(i)
            elif equation[i] == ")":
                if len(opening_indices) == 0:
                    raise Exception(
                        "No opening bracket for closing bracket in {}".format(equation)
                    )
                else:
                    open_idx = opening_indices.pop(-1)
                    new_val = (
                        solve_l_to_r_w_o_brackets(equation[open_idx + 1 : i])
                        if l_to_r
                        else solve_sum_before_prod_w_o_brackets(
                            equation[open_idx + 1 : i]
                        )
                    )
                    equation = equation[:open_idx] + [new_val] + equation[i + 1 :]
                    break

    # if there are more opening brackets than closing ones
    if len(opening_indices) != 0:
        raise Exception("Bracket not closed in {}".format(equation))
    # solve w.o. brackets
    value = (
        solve_l_to_r_w_o_brackets(equation)
        if l_to_r
        else solve_sum_before_prod_w_o_brackets(equation)
    )
    return value


def solve_formulars(
    equations: List[List[Union[str, int]]], l_to_r: bool = True
) -> List[int]:
    """Solve a list of equations"""
    return [solve_l_to_r(equation, l_to_r) for equation in equations]


class Test2020Day18(unittest.TestCase):
    def test_l_to_r(self):
        for formular, result in [
            [["1 + (2 * 3) + (4 * (5 + 6))"], 51],
            [["2 * 3 + (4 * 5)"], 26],
            [["5 + (8 * 3 + 9 + 3 * 4 * 3)"], 437],
            [["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"], 12240],
            [["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"], 13632],
        ]:
            with self.subTest():
                self.assertEqual(
                    sum(solve_formulars(split_formulars(formular))), result
                )

    def test_sum_before_prod(self):
        for formular, result in [
            [["1 + (2 * 3) + (4 * (5 + 6))"], 51],
            [["2 * 3 + (4 * 5)"], 46],
            [["5 + (8 * 3 + 9 + 3 * 4 * 3)"], 1445],
            [["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"], 669060],
            [["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"], 23340],
        ]:
            with self.subTest():
                self.assertEqual(
                    sum(solve_formulars(split_formulars(formular), False)), result
                )


if __name__ == "__main__":
    print(">>> Start Main 18:")
    puzzle_input = load_from_file("data/18.txt")
    puzzle_eq = split_formulars(puzzle_input)
    print("Part 1):")
    print(sum(solve_formulars(puzzle_eq)))
    print("Part 2):")
    print(sum(solve_formulars(puzzle_eq, False)))
    print("End Main 18<<<")
