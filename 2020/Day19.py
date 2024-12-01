import unittest
from typing import Dict, List, Tuple, Set, Union
import itertools
from copy import deepcopy


def load_from_file(filepath: str) -> (List[str], List[str]):
    """load equations from file"""
    with open(filepath) as file:
        rules, messages = file.read().split("\n\n")
    return rules.split("\n"), messages.split("\n")


def read_rules(str_rules: List[str]) -> Dict[int, Union[str, List[Tuple[int, ...]]]]:
    """Read in rules from string"""
    processed = {}
    for rule in str_rules:
        key, val = rule.split(":")
        if val.strip().startswith('"'):
            content = str(val.strip().replace('"', ""))
        else:
            dicts = val.strip().split("|")
            content = [tuple(int(i) for i in d.strip().split(" ")) for d in dicts]
        processed[int(key)] = content
    return processed


def get_possible_strings(
    messages: List[str],
    rule: int,
    rules: Dict[int, Union[str, List[Tuple[int, ...]]]],
    max_recursion_depth: int = 0,
    recursion=None,
) -> Set[str]:
    """checks if a rule and its sublists are valid"""
    # theoretically, one could save all the rule states and reuse them later on (not done)
    if recursion is None:  # default recursion
        recursion = dict()
    # end infinite recursion
    try:
        recursion[rule] += 1
    except KeyError:
        recursion[rule] = 1
    if recursion[rule] > max_recursion_depth:
        return set()
    curr_rules = rules[rule]
    if type(curr_rules) == str:
        return set(curr_rules)
    else:
        # Create combinations of all possible current rules with all possible sub rules
        possible_rules = set()
        for subrules in curr_rules:
            # get content of subrules
            possible_substrings: List[Set[str]] = []
            for i, subrule in enumerate(subrules):
                possible_substrings.append(
                    get_possible_strings(
                        messages,
                        subrule,
                        rules,
                        max_recursion_depth=max_recursion_depth,
                        recursion=deepcopy(recursion),
                    )
                )
            # multiple rules in one subrule: concat in correct order
            # add subrules to all possible rules from this state
            while set() in possible_substrings:
                possible_substrings.remove(set())
            possible_rules.update(
                set(
                    "".join(c for c in l)
                    for l in itertools.product(*possible_substrings)
                )
            )
        # remove items that are no longer possible (to decrease size of tree)
        possible_rules = set(
            pr for pr in possible_rules if any(pr in msg for msg in messages)
        )
        return possible_rules


def check_rule_on_messages(
    messages: List[str],
    rules: Dict[int, Union[str, List[Tuple[int, ...]]]],
    rule: int = 0,
    max_rec: int = 6,
) -> List[bool]:
    """Checks a list of messages on a specific set of rules"""
    possible = get_possible_strings(messages, rule, rules, max_recursion_depth=max_rec)
    return [message in possible for message in messages]


def check_rules_on_single_messages(
    messages: List[str],
    rules: Dict[int, Union[str, List[Tuple[int, ...]]]],
    rule: int = 0,
) -> List[bool]:
    """Checks every single message indepentently"""
    possible = []
    solutions = set()
    for message in messages:
        if message not in solutions:
            # solutions.update(get_possible_strings([message], rule, rules, max_recursion_depth=len(message)))  # to make sure
            solutions.update(
                get_possible_strings([message], rule, rules, max_recursion_depth=10)
            )
        possible.append(message in solutions)
    return possible


class Test2020Day19(unittest.TestCase):
    rules = [
        "42: 9 14 | 10 1",
        "9: 14 27 | 1 26",
        "10: 23 14 | 28 1",
        '1: "a"',
        "11: 42 31",
        "5: 1 14 | 15 1",
        "19: 14 1 | 14 14",
        "12: 24 14 | 19 1",
        "16: 15 1 | 14 14",
        "31: 14 17 | 1 13",
        "6: 14 14 | 1 14",
        "2: 1 24 | 14 4",
        "0: 8 11",
        "13: 14 3 | 1 12",
        "15: 1 | 14",
        "17: 14 2 | 1 7",
        "23: 25 1 | 22 14",
        "28: 16 1",
        "4: 1 1",
        "20: 14 14 | 1 15",
        "3: 5 14 | 16 1",
        "27: 1 6 | 14 18",
        '14: "b"',
        "21: 14 1 | 1 14",
        "25: 1 1 | 1 14",
        "22: 14 14",
        "8: 42",
        "26: 14 22 | 1 20",
        "18: 15 15",
        "7: 14 5 | 1 21",
        "24: 14 1",
    ]
    msgs = [
        "abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa",
        "bbabbbbaabaabba",
        "babbbbaabbbbbabbbbbbaabaaabaaa",
        "aaabbbbbbaaaabaababaabababbabaaabbababababaaa",
        "bbbbbbbaaaabbbbaaabbabaaa",
        "bbbababbbbaaaaaaaabbababaaababaabab",
        "ababaaaaaabaaab",
        "ababaaaaabbbaba",
        "baabbaaaabbaaaababbaababb",
        "abbbbabbbbaaaababbbbbbaaaababb",
        "aaaaabbaabaaaaababaa",
        "aaaabbaaaabbaaa",
        "aaaabbaabbaaaaaaabbbabbbaaabbaabaaa",
        "babaaabbbaaabaababbaabababaaab",
        "aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba",
    ]

    def test_valid_messages(self):
        rules = [
            "0: 4 1 5",
            "1: 2 3 | 3 2",
            "2: 4 4 | 5 5",
            "3: 4 5 | 5 4",
            '4: "a"',
            '5: "b"',
        ]
        msgs = ["ababbb", "bababa", "abbbab", "aaabbb", "aaaabbb"]
        clean_rules = read_rules(rules)
        res = check_rule_on_messages(msgs, clean_rules)
        self.assertListEqual([True, False, True, False, False], res)
        self.assertEqual(sum(res), 2)

    def test_valid_messages_wo_loop(self):
        rules = deepcopy(self.rules)
        msgs = deepcopy(self.msgs)
        clean_rules = read_rules(rules)
        res = check_rule_on_messages(
            msgs, clean_rules, max_rec=max(len(msg) for msg in msgs)
        )
        self.assertEqual(sum(res), 3)

    def test_valid_messages_with_loop(self):
        rules = deepcopy(self.rules)
        msgs = deepcopy(self.msgs)
        rules.remove("8: 42")
        rules.append("8: 42 | 42 8")
        rules.remove("11: 42 31")
        rules.append("11: 42 31 | 42 11 31")
        clean_rules = read_rules(rules)
        res = check_rule_on_messages(msgs, clean_rules)
        self.assertEqual(sum(res), 12)

    def test_valid_messages_with_loop_v2(self):
        rules = deepcopy(self.rules)
        msgs = deepcopy(self.msgs)
        rules.remove("8: 42")
        rules.append("8: 42 | 42 8")
        rules.remove("11: 42 31")
        rules.append("11: 42 31 | 42 11 31")
        clean_rules = read_rules(rules)
        res = check_rules_on_single_messages(msgs, clean_rules, 0)
        self.assertEqual(sum(res), 12)


if __name__ == "__main__":
    print(">>> Start Main 19:")
    puzzle_str_rules, puzzle_messages = load_from_file("data/19.txt")
    puzzle_rules = read_rules(puzzle_str_rules)
    print("Part 1):")
    print(sum(check_rule_on_messages(puzzle_messages, puzzle_rules, 0)))
    print("Part 2):")
    puzzle_rules_str_changed = puzzle_str_rules.copy()
    puzzle_rules_str_changed.remove("8: 42")
    puzzle_rules_str_changed.append("8: 42 | 42 8")
    puzzle_rules_str_changed.remove("11: 42 31")
    puzzle_rules_str_changed.append("11: 42 31 | 42 11 31")
    puzzle_rules_changed = read_rules(puzzle_rules_str_changed)
    print(sum(check_rules_on_single_messages(puzzle_messages, puzzle_rules_changed, 0)))
    print("End Main 19<<<")
