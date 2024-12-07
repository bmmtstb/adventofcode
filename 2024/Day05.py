import math
import unittest

from helper.file import load_file_and_split


Rules = dict[int, list[int]]
Pages = list[int]
Updates = list[Pages]


def load_data(fp: str) -> (Rules, Updates):
    """Load the data from the input file.

    Rules is a dictionary where the key is the page number, and the value is a list of pages that can come after it.
    Pages is a list of integers representing the pages.
    Updates is a list of pages.
    """
    r, p, *_ = load_file_and_split(fp, sep="\n\n")

    rules: Rules = {}
    for rule in r.split("\n"):
        first, second, *_ = rule.split("|")
        if int(first) in rules:
            rules[int(first)].append(int(second))
        else:
            rules[int(first)] = [int(second)]
    pages: Updates = [
        [int(p) for p in page.split(",")] for page in p.split("\n") if len(page)
    ]
    return rules, pages


def is_ordering_correct(rules: Rules, pages: Pages) -> bool:
    """Check if the ordering of the given pages is correct."""
    for i, page in enumerate(pages):
        if page in rules:
            if any(r in pages[:i] for r in rules[page]):
                return False
    return True


def order_correctly(rules: Rules, pages: Pages) -> Pages:
    """Order the pages correctly."""
    for i, page in enumerate(pages):
        if page in rules:
            for r in rules[page]:
                if r in pages[:i]:
                    i_r = pages.index(r)
                    pages.pop(i_r)
                    pages.insert(i, r)
    if is_ordering_correct(rules, pages):
        return pages
    return order_correctly(rules, pages)


def part1(rules: Rules, updates: Updates) -> int:
    """Part1: Return the sum of the middle elements of the pages where the ordering is correct."""
    total = 0
    for pages in updates:
        if is_ordering_correct(rules, pages):
            total += pages[math.floor(len(pages) / 2)]
    return total


def part2(rules: Rules, updates: Updates) -> int:
    """Part2: Return the sum of the middle elements after reordering of the pages where the ordering is incorrect."""
    total = 0
    for pages in updates:
        if not is_ordering_correct(rules, pages):
            reordered = order_correctly(rules, pages)
            total += reordered[math.floor(len(pages) / 2)]
    return total


class Test2024Day05(unittest.TestCase):

    fp = "./data/05-test.txt"
    rules, updates = load_data(fp)

    def test_is_ordering_correct(self):
        for pages, correct in [
            ([75, 47, 61, 53, 29], True),
            ([97, 61, 53, 29, 13], True),
            ([75, 29, 13], True),
            ([75, 97, 47, 61, 53], False),
            ([61, 13, 29], False),
            ([97, 13, 75, 29, 47], False),
        ]:
            with self.subTest(msg="pages: {}, correct: {}".format(pages, correct)):
                self.assertEqual(is_ordering_correct(self.rules, pages), correct)

    def test_order_correctly(self):
        for pages, reordered in [
            ([75, 97, 47, 61, 53], [97, 75, 47, 61, 53]),
            ([61, 13, 29], [61, 29, 13]),
            ([97, 13, 75, 29, 47], [97, 75, 47, 29, 13]),
        ]:
            with self.subTest(msg="pages: {}, reordered: {}".format(pages, reordered)):
                self.assertListEqual(order_correctly(self.rules, pages), reordered)

    def test_p1(self):
        self.assertEqual(part1(self.rules, self.updates), 143)

    def test_p2(self):
        self.assertEqual(part2(self.rules, self.updates), 123)


if __name__ == "__main__":
    print(">>> Start Main 05:")
    puzzle_rules, puzzle_updates = load_data("./data/05.txt")
    print("Part 1): ", part1(puzzle_rules, puzzle_updates))
    print("Part 2): ", part2(puzzle_rules, puzzle_updates))
    print("End Main 05<<<")
