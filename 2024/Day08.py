import unittest

from helper.file import load_file_and_split

Location = tuple[int, int]
Locations = list[Location]


def load_data(fp: str) -> tuple[int, int, dict[str, Locations]]:
    """Read the data and return the height, with, and a dictionary containing the locations for each of the towers."""
    field = load_file_and_split(fp)
    height = len(field)
    width = len(field[0])
    d = {}
    for i, line in enumerate(field):
        for j, char in enumerate(line):
            if char == ".":
                continue
            if char in d:
                d[char].append((i, j))
            else:
                d[char] = [(i, j)]

    return height, width, d


def get_antinode_positions(
    locs: Locations, repeats: int = 1, skip: bool = True
) -> Locations:
    """Get the antinode positions for the given locations.
    Works for part1 and part2, by passing the repeats and skip parameters.

    Args:
        locs (Locations): List of antenna locations.
        repeats (int, optional): The number of repeats in every direction. Defaults to 1.
            Can be simply set to the width or height of the grid.
            Then even antennas with a distance of 1 will be considered.
        skip (bool, optional): Skip the 0 and 1 repeats. Defaults to True for part 1.
    """
    antinodes = []
    if len(locs) == 1:
        return antinodes
    # iterate over all pairs of locations, skipping the same locations and the same pair in reverse order
    for i in range(len(locs) - 1):
        for j in range(i + 1, len(locs)):
            h1, w1 = locs[i]
            h2, w2 = locs[j]
            dh, dw = h2 - h1, w2 - w1
            # the basic case is one repeat from -1 to 2 skipping 0 and 1
            for n in range(-repeats, repeats + 1 + 1):
                if skip and n in [0, 1]:
                    continue
                antinodes.append((h1 + n * dh, w1 + n * dw))

    return antinodes


def part1(fp: str) -> int:
    """Part1: Get the number of unique antinode locations within the grid."""
    height, width, data = load_data(fp)
    all_locs = [
        antinode
        for positions in data.values()
        for antinode in get_antinode_positions(positions)
    ]
    # filter out locations out of bound
    all_locs = {(h, w) for (h, w) in all_locs if 0 <= h < height and 0 <= w < width}
    # get set of list and return length
    return len(all_locs)


def part2(fp: str) -> int:
    """Part2: Do part 1 with all on the same frequency."""
    height, width, data = load_data(fp)
    all_locs = [
        antinode
        for positions in data.values()
        for antinode in get_antinode_positions(
            positions, repeats=max(height, width), skip=False
        )
    ]
    # filter out locations out of bound
    all_locs = {(h, w) for (h, w) in all_locs if 0 <= h < height and 0 <= w < width}
    # get set of list and return length
    return len(all_locs)


class Test2024Day08(unittest.TestCase):

    fp = "./data/08-test.txt"
    test_data = load_data(fp)

    def test_load_data(self):
        height, width, data = self.test_data
        self.assertEqual(height, 12)
        self.assertEqual(width, 12)
        self.assertEqual(len(data.keys()), 2)
        self.assertTrue("A" in data)
        self.assertEqual(len(data["A"]), 3)
        self.assertTrue("0" in data)
        self.assertEqual(len(data["0"]), 4)

    def test_get_antinode_positions(self):
        test_locs = [(1, 1), (2, 1), (1, 2), (2, 2)]
        r = get_antinode_positions(test_locs, repeats=1)
        self.assertEqual(len(r), 12)

        self.assertSetEqual(
            set(r),
            {
                (h, w)
                for h in range(0, 4)
                for w in range(0, 4)
                if (h, w) not in test_locs
            },
        )

    def test_p1(self):
        self.assertEqual(part1(self.fp), 14)

    def test_p2(self):
        self.assertEqual(part2(self.fp), 34)


if __name__ == "__main__":
    print(">>> Start Main 08:")
    print("Part 1): ", part1("./data/08.txt"))
    print("Part 2): ", part2("./data/08.txt"))
    print("End Main 08<<<")
