import unittest

from helper.file import read_lines_as_list


def load_data(fp: str) -> list[list[int]]:
    """Read all reports."""
    return read_lines_as_list(fp, instance_type=int, split=" ")


def is_report_safe(report: list[int]) -> bool:
    """Check if the report is safe."""
    if len(report) == 0:
        raise NotImplementedError("Empty reports are not supported.")
    if len(report) == 1:
        return True
    differences = [report[i + 1] - report[i] for i in range(len(report) - 1)]
    return all(0 < abs(diff) <= 3 for diff in differences) and (
        all(d > 0 for d in differences) or all(d < 0 for d in differences)
    )


def is_report_tolerable(report: list[int]) -> bool:
    """Check if the report is tolerable."""
    permutations = [report] + [report[:i] + report[i + 1 :] for i in range(len(report))]
    return any(is_report_safe(p) for p in permutations)


def part1(reports: list[list[int]]) -> int:
    """Count the number of safe reports."""
    return sum(is_report_safe(report) for report in reports)


def part2(reports: list[list[int]]) -> int:
    """Count the number of tolerable reports."""
    return sum(is_report_tolerable(report) for report in reports)


class Test2024Day002(unittest.TestCase):
    fp = "./data/02-test.txt"
    data = load_data(fp)
    puzzle_input = load_data("./data/02.txt")

    def test_load_data(self):
        self.assertTrue(isinstance(self.data, list))
        self.assertEqual(len(self.data), 6)
        self.assertTrue(all(len(d) == 5 for d in self.data))

    def test_is_report_safe(self):
        for i, is_safe in enumerate([True, False, False, False, False, True]):
            with self.subTest(msg=f"i: {i}, is_safe: {is_safe}"):
                self.assertEqual(is_report_safe(self.data[i]), is_safe)

    def test_is_report_tolerable(self):
        for i, is_safe in enumerate([True, False, False, True, True, True]):
            with self.subTest(msg=f"i: {i}, is_safe: {is_safe}"):
                self.assertEqual(is_report_tolerable(self.data[i]), is_safe)

    def test_part1(self):
        self.assertEqual(part1(self.data), 2)
        self.assertEqual(part1(self.puzzle_input), 356)

    def test_part2(self):
        self.assertEqual(part2(self.data), 4)
        self.assertEqual(part2(self.puzzle_input), 413)


if __name__ == "__main__":
    print(">>> Start Main 002:")
    puzzle_input = load_data("./data/02.txt")
    print("Part 1): ", part1(puzzle_input))
    print("Part 2): ", part2(puzzle_input))
    print("End Main 002<<<")
