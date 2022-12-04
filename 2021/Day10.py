import unittest
from typing import Dict, List, Tuple, Set, Union

from helper.file import read_lines_as_list

scores_corrupt: Dict[str, int] = {
    None: 0,
    ")":  3,
    "]":  57,
    "}":  1197,
    ">":  25137,
}

scores_missing: Dict[str, int] = {
    ")":  1,
    "]":  2,
    "}":  3,
    ">":  4,
}

counter: Dict[str, str] = {
    "(": ")",
    "<": ">",
    "{": "}",
    "[": "]",
    ")": "(",
    ">": "<",
    "}": "{",
    "]": "["
}


def is_line_corrupted(line: str, return_open: bool = False) -> Union[str, List[str], None]:
    """returns a bracket if a line is corrupted"""
    open_brackets = []
    for char in line:
        if char in ["<", "(", "{", "["]:
            open_brackets.append(char)
        elif char in [">", ")", "}", "]"]:
            if not len(open_brackets) >= 1:
                return char
            elif counter[char] != open_brackets[-1]:
                return char
            else:
                open_brackets.pop(-1)
        else:
            raise Exception("Invalid character {}".format(char))
    if return_open:  # return stack of open brackets for further analysis
        return open_brackets
    return None


def calculate_line_missing(line: str) -> Union[str, bool, None]:
    """if there are brackets missing at the end, return them, return False if corrupted"""
    open_brackets = is_line_corrupted(line, return_open=True)
    if type(open_brackets) is str:
        return False
    elif open_brackets is None or len(open_brackets) == 0:
        return None
    else:
        open_brackets.reverse()  # close last ones first
        return "".join(counter[bracket] for bracket in open_brackets)


def calculate_line_missing_cost(missing: str) -> int:
    """calculate the missing lines cost"""
    "Start with a total score of 0. Then, for each character, multiply the total score by 5 and then increase the "
    "total score by the point value given "
    line_score = 0
    for char in missing:
        line_score *= 5
        line_score += scores_missing[char]
    return line_score


class Test2021Day10(unittest.TestCase):
    test_data = ["[({(<(())[]>[[{[]{<()<>>",
                 "[(()[<>])]({[<{<<[]>>(",
                 "{([(<{}[<>[]}>{[]{[(<()>",
                 "(((({<>}<{<{<>}{[]{[]{}",
                 "[[<[([]))<([[{}[[()]]]",
                 "[{[{({}]{}}([{[{{{}}([]",
                 "{<[[]]>}<{[{[{[]{()[[[]",
                 "[<(<(<(<{}))><([]([]()",
                 "<{([([[(<>()){}]>(<<{{",
                 "<{([{{}}[<[[[<>{}]]]>[]]"]
    test_corruption = [None, None, "}", None, ")", "]", None, ")", ">", None]
    test_missing = ["}}]])})]", ")}>]})", False, "}}>}>))))", False, False, "]]}}]}]}>", False, False, "])}>"]
    test_missing_cost = [288957, 5566, False, 1480781, False, False, 995444, False, False, 294]

    def test_custom_corrupted(self):
        for test_line, corruption in [
            ["]", "]"],
            ["[]]", "]"],
            ["[]]}", "]"],
            ["[]]}", "]"],
            ["{[]}", None],
            ["[[]]}", "}"],
        ]:
            with self.subTest():
                self.assertEqual(is_line_corrupted(test_line), corruption)

    def test_corrupted_examples(self):
        for i, line in enumerate(self.test_data):
            self.assertEqual(is_line_corrupted(line), self.test_corruption[i])

    def test_custom_missing(self):
        for test_line, missing in [
            ["[", "]"],
            ["[][", "]"],
            ["[]}", False],
            ["(<[{", "}]>)"],
            ["{[]}", None],
            ["<{[[]]{}", "}>"],
        ]:
            with self.subTest():
                self.assertEqual(calculate_line_missing(test_line), missing)

    def test_missing_examples(self):
        for i, line in enumerate(self.test_data):
            self.assertEqual(calculate_line_missing(line), self.test_missing[i])

    def test_calculate_missing_cost(self):
        for i, missing_chars in enumerate(self.test_missing):
            if self.test_missing[i]:
                self.assertEqual(calculate_line_missing_cost(missing_chars), self.test_missing_cost[i])


if __name__ == '__main__':
    print(">>> Start Main 10:")
    puzzle_input = read_lines_as_list("data/10.txt")
    puzzle_corrupt = [is_line_corrupted(line) for line in puzzle_input.copy()]
    print("Part 1): ", sum(scores_corrupt[res] for res in puzzle_corrupt))
    puzzle_missing = [calculate_line_missing(line) for line in puzzle_input.copy()]
    cost = [calculate_line_missing_cost(line) for line in puzzle_missing if type(line) is str]
    cost.sort()
    print("Part 2): ", cost[int(len(cost) / 2)])
    print("End Main 10<<<")
