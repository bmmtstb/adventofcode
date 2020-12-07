import unittest
from parameterized import parameterized
from typing import Dict, List, Tuple, Set

own_bag = "shiny gold"
leaf_node = "no other"


def read_file_in_groups(filepath: str) -> Dict[str, Dict[str, int]]:
    """reads the file at filepath"""
    rules = {}
    with open(filepath) as file:
        for line in file.readlines():
            ls, rs = line.replace("\n", "").replace(".", "").split(" contain ")
            ls_bag = ls.strip().replace(" bags", "")
            rs_bags = rs.strip().replace(" bags", "").replace(" bag", "").split(",")
            if rs_bags[0] == leaf_node:
                rs_bags[0] = "0 " + rs_bags[0]
            rules[ls_bag] = {" ".join(bag.strip().split(" ")[1:]): int(bag.strip().split(" ")[0]) for bag in rs_bags}
    return rules


def can_contain(dependencies: Dict[str, Dict[str, int]], goals=None) -> Set[str]:
    """Check how many different parents there are for a specific node"""
    if goals is None:
        goals = [own_bag]
    colors_of_containing_bags = set()
    for goal in goals:
        subgoals = []
        # find current goal in dependencies
        for rule_k, rule_v in dependencies.items():
            if goal in rule_v.keys():
                subgoals.append(rule_k)
                colors_of_containing_bags.add(rule_k)
        # find the possible solutions for all the subgoals found
        # definitely not performant
        if len(subgoals) > 0:
            colors = can_contain(dependencies, subgoals)
            colors_of_containing_bags = colors_of_containing_bags.union(colors)
    return colors_of_containing_bags


def count_child_nodes(tree: Dict[str, Dict[str, int]], goal: str = own_bag) -> int:
    """Count the number of bags necessary to buy for the given node"""
    nof_bags = 0
    if goal == leaf_node:
        return 0
    for node_k, node_v in tree.items():
        if node_k == goal:
            # add and multiply recursive results for every child
            for child_k, multiplicator in node_v.items():
                nof_bags += multiplicator * (1 + count_child_nodes(tree, child_k))
    return nof_bags


class Test2020Day07(unittest.TestCase):
    test_input1 = read_file_in_groups("data/07-test.txt")
    test_input2 = read_file_in_groups("data/07-test2.txt")

    @parameterized.expand([
        [test_input1, 4],
    ])
    def test_count_parents(self, data, contain):
        self.assertEqual(len(can_contain(data)), contain)

    @parameterized.expand([
        [test_input1, own_bag, 32],
        [test_input1, "faded blue", 0],
        [test_input1, "dotted black", 0],
        [test_input1, "vibrant plum", 11],
        [test_input1, "dark olive", 7],
        [test_input2, own_bag, 126],
    ])
    def test_number_of_bags(self, data, goal, bags):
        self.assertEqual(count_child_nodes(data, goal=goal), bags)


if __name__ == '__main__':
    print(">>> Start Main 07:")
    puzzle_input = read_file_in_groups("data/07.txt")
    print("Part 1):")
    print(len(can_contain(puzzle_input)))
    print("Part 2):")
    print(count_child_nodes(puzzle_input))
    print("End Main 07<<<")
