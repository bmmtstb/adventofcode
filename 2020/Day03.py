import unittest
from parameterized import parameterized

vegetation_map = {
    ".": 0,
    "#": 1,
}


def load_data(filepath="/data/03.txt"):
    map = []
    with open(filepath) as file:
        for line in file.readlines():
            map.append([vegetation_map[c] for c in line.removesuffix("\n")])
    return map


def obstacles_in_path(data, horizontal=3, vertical=1):
    """Count the number of obstacles on the path given by the stepsize"""
    obstacles = 0
    pos = (0, 0)
    h, w = len(data), len(data[0])  # height and width of the map
    while pos[1] < len(data):
        if data[pos[1]][pos[0] % w] > 0:
            obstacles += 1
        pos = (pos[0] + horizontal, pos[1] + vertical)
    return obstacles


class TestDay03(unittest.TestCase):
    @parameterized.expand([
        ["data/03-Test.txt", 1, 1, 2],
        ["data/03-Test.txt", 3, 1, 7],
        ["data/03-Test.txt", 5, 1, 3],
        ["data/03-Test.txt", 7, 1, 4],
        ["data/03-Test.txt", 1, 2, 2],
    ])
    def test_single_slope(self, fname, right, down, obs):
        self.assertEqual(obstacles_in_path(load_data(fname), horizontal=right, vertical=down), obs)


if __name__ == '__main__':
    print(">>> Start Main 03:")
    puzzle_input = load_data("data/03.txt")
    print("Part 1):")
    print(obstacles_in_path(puzzle_input))
    print("Part 2):")
    mult = obstacles_in_path(puzzle_input, 1, 1) * obstacles_in_path(puzzle_input, 3, 1) * \
           obstacles_in_path(puzzle_input, 5, 1) * obstacles_in_path(puzzle_input, 7, 1) * \
           obstacles_in_path(puzzle_input, 1, 2)
    print(mult)
    print("End Main 03<<<")
