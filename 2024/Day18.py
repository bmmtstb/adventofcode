import heapq
import unittest

from helper.file import read_lines_as_list
from helper.tuple import manhattan_distance, tuple_add_tuple

Coordinate = tuple[int, int]  # X, Y (distance from left, distance from top)
Coordinates = list[Coordinate]

neighbors = [
    (0, 1),  # right
    (1, 0),  # down
    (0, -1),  # left
    (-1, 0),  # up
]


def load_data(fp: str) -> Coordinates:
    return [tuple(c) for c in read_lines_as_list(fp, inst=int, split=",")]


def a_star(forbidden: Coordinates, target: Coordinate) -> int:
    open_list: list[tuple[int, Coordinate]] = []
    heapq.heappush(open_list, (0, (0, 0)))

    g: dict[Coordinate, int] = {(0, 0): 0}

    closed_list: set[Coordinate] = set(forbidden)

    while len(open_list) > 0:
        current: Coordinate
        _, current = heapq.heappop(open_list)
        if current == target:
            return g[target]
        closed_list.add(current)
        # Get neighbors / expand node
        for neigh_dist in neighbors:
            neighbor = tuple_add_tuple(current, neigh_dist)

            # skip if neighbor is out of bounds
            if neighbor[0] < 0 or neighbor[1] < 0:
                continue
            if neighbor[0] > target[0] or neighbor[1] > target[1]:
                continue

            # skip if neighbor is forbidden or has been analyzed
            if neighbor in closed_list:
                continue

            tentative_g = g[current] + 1
            # skip if there is a better path already in the open list
            if any(c == neighbor and tentative_g >= g[neighbor] for v, c in open_list):
                continue
            # update g and f
            g[neighbor] = tentative_g
            f = tentative_g + manhattan_distance(neighbor, target)  # f = g + h
            if any(c == neighbor for _, c in open_list):
                for i, (k, v) in enumerate(open_list):
                    if v == neighbor:
                        open_list.pop(i)
                        heapq.heappush(open_list, (f, neighbor))
                        break
            else:
                heapq.heappush(open_list, (f, neighbor))

    return -1


def part1(coords: Coordinates, bytes_fallen: int, target: Coordinate) -> int:
    """Part1: Get the minimum number of steps to get from the top left to the bottom right."""

    return a_star(forbidden=coords[:bytes_fallen], target=target)


def part2(coords: Coordinates, bytes_fallen: int, target: Coordinate) -> Coordinate:
    """Part2: Find the position of the first byte that blocks all paths."""
    for i in range(bytes_fallen + 1, len(coords)):
        # get the coordinates of the byte
        # check if the byte is blocking all paths
        if a_star(forbidden=coords[: i + 1], target=target) == -1:
            return coords[i]
    return -1, -1


class Test2024Day18(unittest.TestCase):

    fp = "./data/18-test.txt"
    test_data = load_data(fp)

    def test_p1(self):
        self.assertEqual(part1(self.test_data, bytes_fallen=12, target=(6, 6)), 22)

    def test_p2(self):
        self.assertEqual(part2(self.test_data, bytes_fallen=12, target=(6, 6)), (6, 1))


if __name__ == "__main__":
    print(">>> Start Main 18:")
    puzzle_data = load_data("./data/18.txt")
    print("Part 1): ", part1(puzzle_data, bytes_fallen=1024, target=(70, 70)))
    print("Part 2): ", part2(puzzle_data, bytes_fallen=1024, target=(70, 70)))
    print("End Main 18<<<")
