import unittest
from typing import Dict, List, Tuple, Set

from helper.file import read_lines_as_list
from helper.tuple import tuple_add_tuple

Map = List[List[int]]


def get_lowest_adjacent(height_map: Map, x: int, y: int, exclude: List[Tuple[int, int]] = None) -> int:
    """given a position in the grid, calculate the min height of the adjacent neighbors"""
    if exclude is None:
        exclude = []
    poss = [10]  # add invalid value to never call min() on empty list
    if 0 <= x - 1 and (x-1, y) not in exclude:
        poss.append(height_map[y][x-1])
    if x + 1 < len(height_map[0]) and (x+1, y) not in exclude:
        poss.append(height_map[y][x+1])
    if 0 <= y - 1 and (x, y-1) not in exclude:
        poss.append(height_map[y - 1][x])
    if y + 1 < len(height_map) and (x, y+1) not in exclude:
        poss.append(height_map[y + 1][x])
    return min(poss)


def find_low_points(height_map: Map) -> List[Tuple[int, int, int]]:
    """given a map locate local optima, return height + pos"""
    minima = []
    for curr_y in range(len(height_map)):
        for curr_x in range(len(height_map[0])):
            if height_map[curr_y][curr_x] < get_lowest_adjacent(height_map, curr_x, curr_y):
                minima.append((height_map[curr_y][curr_x], curr_x, curr_y))
    return minima


def get_basin_size(height_map: Map, x: int, y: int) -> int:
    """find the size of a basin with minimum at (x,y) [9 does not count]"""
    neighbors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    basin_points: List[Tuple[int, int]] = [(x, y)]
    new_added = True
    while new_added:
        new_added = False
        for point in basin_points:
            # if current point has neighbors != 9 add them
            if get_lowest_adjacent(height_map, point[0], point[1], exclude=basin_points) < 9:
                # add all points that have not been analyzed yet
                for neighbor in neighbors:
                    neighbor_coord = tuple_add_tuple(point, neighbor)
                    # point hasn't been analyzed yet and is in bounds and is no maximum
                    if neighbor_coord not in basin_points and \
                            0 <= neighbor_coord[0] < len(height_map[0]) and \
                            0 <= neighbor_coord[1] < len(height_map) and \
                            height_map[neighbor_coord[1]][neighbor_coord[0]] < 9:
                        basin_points.append(neighbor_coord)
                        new_added = True
    return len(basin_points)


class Test2021Day09(unittest.TestCase):
    def test_lowest_adjacent(self):
        for tx, ty, lowest in [
            [0, 0, 1],
            [1, 0, 2],
            [1, 1, 1],
        ]:
            with self.subTest():
                test_input = [[int(val) for val in line] for line in read_lines_as_list("data/09-test.txt", instance_type=list)]
                self.assertEqual(get_lowest_adjacent(test_input, tx, ty), lowest)

    def test_find_optima(self):
        test_input = [[int(val) for val in line] for line in read_lines_as_list("data/09-test.txt", instance_type=list)]
        low_points = find_low_points(test_input)
        self.assertEqual(sum(val[0] + 1 for val in low_points), 15)
        self.assertTupleEqual(low_points[0][1:], (1, 0))

    def test_basin_size(self):
        for x, y, size in [
            [1, 0, 3],
            [9, 0, 9],
            [2, 2, 14],
            [6, 4, 9],
        ]:
            with self.subTest():
                test_input = [[int(val) for val in line] for line in read_lines_as_list("data/09-test.txt", instance_type=list)]
                self.assertEqual(get_basin_size(test_input, x, y), size)


if __name__ == '__main__':
    print(">>> Start Main 09:")
    puzzle_input = [[int(val) for val in line] for line in read_lines_as_list("data/09.txt", instance_type=list)]
    low_points = find_low_points(puzzle_input)
    print("Part 1): ", sum(val[0] + 1 for val in low_points))

    basin_sizes = [get_basin_size(puzzle_input, line[1], line[2]) for line in low_points]
    basin_sizes.sort(reverse=True)
    print("Part 2): ", basin_sizes[0] * basin_sizes[1] * basin_sizes[2])
    print("End Main 09<<<")
