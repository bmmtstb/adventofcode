import unittest
from typing import Dict, List


def load(filepath: str) -> List[int]:
    """load the file"""
    data = []
    with open(filepath) as file:
        for l in file.readlines():
            data.append(int(l))
    return data


def get_adapter_differences(adapters: List[int]) -> Dict[int, int]:
    """calculate Adapter differences using all adapters"""
    sorted_adapters = adapters.copy() + [0, max(adapters) + 3]
    sorted_adapters.sort()
    differences = [
        sorted_adapters[c + 1] - sorted_adapters[c]
        for c in range(len(sorted_adapters) - 1)
    ]
    return {val: differences.count(val) for val in set(differences)}


# def get_different_arrangements(adapters: List[int], node: int = 0) -> int:
#     """Count all possible arrangements of the adapters"""
#     if node == max(adapters):
#         return 1
#
#     counter = 0
#
#     possible_node_combinations = [i for i in adapters if 1 <= i - node <= 3]
#     for comb_node in possible_node_combinations:
#         counter += get_different_arrangements(adapters, comb_node)
#
#     return counter


def get_different_arrangements(adapters: List[int]) -> int:
    """Count all possible arrangements of the adapters"""
    sorted_adapters = adapters.copy() + [0, max(adapters) + 3]
    sorted_adapters.sort()

    possible_combinations = {}
    for node in sorted_adapters[:-1]:
        possible_combinations[node] = [i for i in sorted_adapters if 1 <= i - node <= 3]

    sorted_adapters.sort(reverse=True)
    comb_of_val = {sorted_adapters[0]: 1}
    for node in sorted_adapters[1:]:
        if node in comb_of_val.keys():
            comb_of_val[node] += sum(
                comb_of_val[key] for key in possible_combinations[node]
            )
        else:
            comb_of_val[node] = sum(
                comb_of_val[key] for key in possible_combinations[node]
            )
    return comb_of_val[0]


class Test2020Day10(unittest.TestCase):
    def test_list_differences(self):
        for adapters, differences, arr in [
            [[16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4], {1: 7, 3: 5}, 8],
            [load("data/10-test.txt"), {1: 22, 3: 10}, 19208],
        ]:
            with self.subTest():
                self.assertEqual(get_adapter_differences(adapters), differences)
                self.assertEqual(get_different_arrangements(adapters), arr)


if __name__ == "__main__":
    print(">>> Start Main 10:")
    puzzle_input = load("data/10.txt")
    print("Part 1):")
    diffs = get_adapter_differences(puzzle_input)
    print(diffs)
    print(diffs[1] * diffs[3])
    print("Part 2):")
    print(get_different_arrangements(puzzle_input))
    print("End Main 10<<<")
