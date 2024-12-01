import unittest

from helper.file import read_lines_as_list


def import_file(filepath: str) -> tuple[tuple[int, ...], tuple[int, ...]]:
    data = read_lines_as_list(filepath=filepath, instance_type=int, split="   ")
    return tuple(zip(*data))


def part1(data: tuple[tuple[int, ...], tuple[int, ...]]) -> int:
    """Return the sorted distance between the two tuples."""
    l1, l2 = list(data[0]), list(data[1])
    l1.sort()
    l2.sort()
    return sum(abs(x - y) for x, y in zip(l1, l2))


def part2(data: tuple[tuple[int, ...], tuple[int, ...]]) -> int:
    """Return the similarity score between the two tuples."""
    l1, l2 = list(data[0]), list(data[1])
    similarities: dict[int, int] = {}
    for val in l1:
        if val in similarities:
            continue

        similarities[val] = sum(1 for l2_i in l2 if l2_i == val)
    return sum(similarities[l1_i] * l1_i for l1_i in l1)


class Test2024Day001(unittest.TestCase):

    test_file = './data/01-test.txt'
    test_data = import_file(test_file)

    def test_load_data(self):
        self.assertEqual(self.test_data, ((3, 4, 2, 1, 3, 3), (4, 3, 5, 3, 9, 3)))

    def test_part1(self):
        self.assertEqual(part1(self.test_data), 11)

    def test_part2(self):
        self.assertEqual(part2(self.test_data), 31)


if __name__ == '__main__':
    print(">>> Start Main 001:")
    puzzle_input = import_file('./data/01.txt')
    print("Part 1): ", part1(puzzle_input))
    print("Part 2): ", part2(puzzle_input))
    print("End Main 001<<<")
