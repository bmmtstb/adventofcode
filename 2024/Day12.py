import unittest

from helper.file import read_lines_as_list
from helper.tuple import tuple_add_tuple

Position = tuple[int, int]
Positions = set[Position]

directions: Positions = {(-1, 0), (1, 0), (0, -1), (0, 1)}


def load_data(fp: str) -> list[str]:
    """Read the data the given from file, returning one string per row."""
    return read_lines_as_list(fp)


def get_plot_by_position(data: list[str], pos: Position, plot: Positions = None) -> Positions:
    """Get the continuous plot at the given position."""
    if plot is None:
        plot: Positions = {pos}

    curr_char = data[pos[0]][pos[1]]

    for d in directions:
        neighbor_pos = tuple_add_tuple(pos, d)
        # skip plot if already visited or out of bounds
        if neighbor_pos in plot or not (0 <= neighbor_pos[0] < len(data) and 0 <= neighbor_pos[1] < len(data[0])):
            continue

        # check whether the neighbor has the same type as the current plot
        if data[neighbor_pos[0]][neighbor_pos[1]] == curr_char:
            plot = plot.union({neighbor_pos})
            plot = plot.union(get_plot_by_position(data, pos=neighbor_pos, plot=plot))

    return plot


def get_plot_fencing_price(plot: Positions, bulk_discount: bool = False) -> int:
    """Get the fencing price of the plot."""

    perimeter = 0

    for field in plot:
        for d in directions:

            neighbor_pos = tuple_add_tuple(field, d)
            if neighbor_pos not in plot:
                perimeter += 1

        # handle bulk discount
        if bulk_discount:
            if (
                tuple_add_tuple(field, (0, -1)) in plot
                and tuple_add_tuple(field, (-1, -1)) not in plot
                and tuple_add_tuple(field, (-1, 0)) not in plot
            ):
                perimeter -= 1
            if (
                tuple_add_tuple(field, (-1, 0)) in plot
                and tuple_add_tuple(field, (-1, 1)) not in plot
                and tuple_add_tuple(field, (0, 1)) not in plot
            ):
                perimeter -= 1
            if (
                tuple_add_tuple(field, (0, 1)) in plot
                and tuple_add_tuple(field, (1, 1)) not in plot
                and tuple_add_tuple(field, (1, 0)) not in plot
            ):
                perimeter -= 1
            if (
                tuple_add_tuple(field, (1, 0)) in plot
                and tuple_add_tuple(field, (1, -1)) not in plot
                and tuple_add_tuple(field, (0, -1)) not in plot
            ):
                perimeter -= 1

    # area is the number of fields in the plot
    # perimeter is the number of neighbors that are not in the plot
    return len(plot) * perimeter


def part1(data: list[str]) -> int:
    """Part1: Get the total fencing price."""
    visited: Positions = set()
    total_fencing_price = 0

    for i, row in enumerate(data):
        for j in range(len(row)):
            # skip already analyzed plots
            if (i, j) in visited:
                continue

            plot = get_plot_by_position(data, pos=(i, j))
            total_fencing_price += get_plot_fencing_price(plot)

            visited = visited.union(plot)

    return total_fencing_price


def part2(data: list[str]) -> int:
    """Part2: Get the total fencing price with bulk discount."""
    visited: Positions = set()
    total_fencing_price = 0

    for i, row in enumerate(data):
        for j in range(len(row)):
            # skip already analyzed plots
            if (i, j) in visited:
                continue

            plot = get_plot_by_position(data, pos=(i, j))
            total_fencing_price += get_plot_fencing_price(plot, bulk_discount=True)

            visited = visited.union(plot)

    return total_fencing_price


class Test2024Day12(unittest.TestCase):

    fp = "./data/12-test.txt"
    test_data = load_data(fp)

    def test_get_plot_by_position(self):
        for pos, result in [
            (
                (0, 0),
                {(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 2), (2, 3), (2, 4), (3, 2)},
            ),  # R
            (
                (1, 1),
                {(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 2), (2, 3), (2, 4), (3, 2)},
            ),  # R
            ((4, 7), {(4, 7)}),  # single C mid right
        ]:
            with self.subTest(msg="pos: {}, result: {}".format(pos, result)):
                self.assertSetEqual(get_plot_by_position(self.test_data, pos), result)

    def test_get_plot_fencing_price(self):
        for char, pos, result, bulk_res in [
            ("R", (0, 0), 216, 120),
            ("I", (0, 4), 32, 16),
            ("C_up_r", (0, 6), 392, 308),
            ("F", (0, 8), 180, 120),
            ("V", (2, 0), 260, 130),
            ("J", (3, 6), 220, 132),
            ("C_mid_r", (4, 7), 4, 4),
            ("E", (4, 9), 234, 104),
            ("I", (5, 2), 308, 224),
            ("M", (7, 0), 60, 30),
            ("S", (8, 4), 24, 18),
        ]:
            with self.subTest(msg="char: {}, pos: {}, result: {}".format(char, pos, result)):
                plot = get_plot_by_position(self.test_data, pos=pos)
                self.assertEqual(get_plot_fencing_price(plot), result)
                self.assertEqual(get_plot_fencing_price(plot, bulk_discount=True), bulk_res)

    def test_p1(self):
        self.assertEqual(part1(self.test_data), 1930)

    def test_p2(self):
        self.assertEqual(part2(self.test_data), 1206)


if __name__ == "__main__":
    print(">>> Start Main 12:")
    puzzle_data = load_data("./data/12.txt")
    print("Part 1): ", part1(puzzle_data))
    print("Part 2): ", part2(puzzle_data))
    print("End Main 12<<<")
