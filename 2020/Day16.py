import unittest
from typing import Dict, List, Tuple, Set
from copy import deepcopy


def load_dataset(filepath: str) -> (Dict[str, Tuple[Tuple[int, int], Tuple[int, int]]], List[int], List[List[int]]):
    """load single document dataset"""
    step = 0
    rules = {}
    own = []
    tickets = []
    with open(filepath) as file:
        for line in file.readlines():
            if line == "\n":
                step += 1
            else:
                line.replace("\n", "")
                if "ticket" in line:
                    continue
                if step == 0:
                    rule, bound_string = line.split(":")
                    l, r = bound_string.strip().split(" or ")
                    l1, l2 = l.split("-")
                    r1, r2 = r.split("-")
                    l_int = (int(l1), int(l2))
                    r_int = (int(r1), int(r2))
                    rules[str(rule)] = (l_int, r_int)
                elif step == 1:
                    own = [int(num) for num in line.split(",")]
                elif step == 2:
                    tickets.append([int(num) for num in line.split(",")])

    return rules, own, tickets


def get_is_ticket_valid(ticket: List[int], rules: Dict[str, Tuple[Tuple[int, int], Tuple[int, int]]]) -> bool:
    """returns true if a ticket is valid"""
    for val in ticket:
        if not any(rule_tup[0][0] <= val <= rule_tup[0][1] or rule_tup[1][0] <= val <= rule_tup[1][1] for rule_tup in
                   rules.values()):
            return False
    return True


def get_ticket_scanning_error_rate(tickets: List[List[int]], rules: Dict[str, Tuple[Tuple[int, int], Tuple[int, int]]]) -> int:
    """Calculate value sum of tickets with wrong values"""
    error = 0
    for ticket in tickets:
        for num in ticket:
            if not any(rule_tup[0][0] <= num <= rule_tup[0][1] or rule_tup[1][0] <= num <= rule_tup[1][1] for rule_tup in rules.values()):
                error += num
    return error


def get_correct_tickets(tickets: List[List[int]], rules: Dict[str, Tuple[Tuple[int, int], Tuple[int, int]]]) -> List[List[int]]:
    """get the list of correct tickets"""
    correct = []
    for ticket in tickets:
        if get_is_ticket_valid(ticket, rules) and len(ticket) == len(rules):
            correct.append(ticket)
    return correct


def get_matching_rules(tickets: List[List[int]], rules: Dict[str, Tuple[Tuple[int, int], Tuple[int, int]]]) -> Dict[str, int]:
    """Match every rule with one row of values"""
    # if len(tickets) > len(rules):
    #     raise Exception("There are to many rules, please double check")
    # get every matching column for every rule
    matches: Dict[str, List[int, ...]] = {}
    for rule_name, rule_tup in rules.items():
        for i in range(len(tickets[0])):
            if all(rule_tup[0][0] <= t[i] <= rule_tup[0][1] or rule_tup[1][0] <= t[i] <= rule_tup[1][1] for t in tickets):
                if rule_name in matches:
                    matches[rule_name].append(i)
                else:
                    matches[rule_name] = [i]
    definitions = {}
    # as long as there are items with more than one rule assigned (all the others will be removed)
    while len(matches) > 0 and len(definitions) < len(rules):
        new_matches: Dict[str, List[int]] = deepcopy(matches)
        for match_name, match_indices in matches.items():
            # if len(match_indices) == 0:
            #     raise Exception("There are no more matching rules for {}".format(match_name))
            # remove every index that has only one matching rule, and delete this rule from all others
            if len(match_indices) == 1:
                def_index = new_matches.pop(match_name)[0]
                definitions[match_name] = def_index
                for new_match_indices in new_matches.values():
                    if def_index in new_match_indices:
                        new_match_indices.remove(def_index)
                # exit for loop with inconsistent state
                break
        if matches == new_matches:
            print("equal states")
            break
        matches = new_matches
    return definitions



class Test2020Day16(unittest.TestCase):
    def test_error_rate(self):
        rules, own, tickets = load_dataset("data/16-test.txt")
        self.assertEqual(get_ticket_scanning_error_rate(tickets, rules), 71)

    def test_find_matches(self):
        rules, own, tickets = load_dataset("data/16-test2.txt")
        correct = get_correct_tickets(tickets, rules)
        self.assertListEqual(correct, tickets[:-1])
        self.assertDictEqual(get_matching_rules(correct, rules), {"class": 1, "row": 0, "seat": 2})


if __name__ == '__main__':
    print(">>> Start Main 16:")
    puzzle_rules, puzzle_own, puzzle_tickets = load_dataset("data/16.txt")
    print("Part 1):")
    print(get_ticket_scanning_error_rate(puzzle_tickets, puzzle_rules.copy()))
    print("Part 2):")
    puzzle_correct = get_correct_tickets(puzzle_tickets, puzzle_rules.copy())
    # get every matching rule for every column in the tickets
    puzzle_matching = get_matching_rules(puzzle_correct, puzzle_rules.copy())
    matching_own_values = {k: puzzle_own[v] for k, v in puzzle_matching.items()}
    print(matching_own_values)
    prod = 1
    for key, value in puzzle_matching.items():
        if key.startswith("departure"):
            prod *= puzzle_own[value]
    print(prod)
    print("End Main 16<<<")
