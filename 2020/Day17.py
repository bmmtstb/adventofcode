import unittest
from copy import deepcopy

from typing import List, Tuple, Union

from helper.tuple import tuple_add_tuple

nof_dimensions = 3
directions_3d = [(l, k, j) for j in range(-1, 2) for k in range(-1, 2) for l in range(-1, 2) if not (l == k == j == 0)]
directions_4d = [(m, l, k, j) for j in range(-1, 2) for k in range(-1, 2) for l in range(-1, 2) for m in range(-1, 2) if not (l == k == j == m == 0)]


def symbols_to_bool(data: List[str], dim: int = 3) -> Union[List[List[List[bool]]], List[List[List[List[bool]]]]]:
    """transform given data to nested bool list"""
    d = []
    for row in data:
        d.append([char == "#" for char in row])
    if dim == 3:
        return [d]
    elif dim == 4:
        return [[d]]
    else:
        raise Exception("only 3 and 4 dimensional")


def run_cycle_3d(data: List[List[List[bool]]]):
    """Cubes chances their state simultaneously"""

    # with a little help from day 11
    def adjacent_neighbors(d, r, c, n):  # row col nested
        """calculate the types of adjacent seats"""
        seeing_types = {True: 0, False: 0}
        # for every 3D neighbor
        for dire in directions_3d:
            neigh_val = get_neighbor_in_direction(d, (r, c, n), dire)
            if not (neigh_val is None):
                seeing_types[neigh_val] += 1
        return seeing_types

    def get_neighbor_in_direction(d, pos: Tuple[int, int, int], direction: Tuple[int, int, int]) -> bool:
        """get the neighboring element in the direction"""
        i, j, k = tuple_add_tuple(pos, direction)
        return d[i][j][k] if 0 <= i < len(d) and 0 <= j < len(d[i]) and 0 <= k < len(d[i][j]) else None

    # calculate new active states
    new_data = deepcopy(data)
    for r_i, row in enumerate(new_data):
        for c_i, col in enumerate(row):
            for z_i, nested in enumerate(col):
                # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive. If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes
                # active. Otherwise, the cube remains inactive.
                neighbors = adjacent_neighbors(data, r_i, c_i, z_i)
                if data[r_i][c_i][z_i] and 2 <= neighbors[True] <= 3:
                    new_data[r_i][c_i][z_i] = True
                elif not data[r_i][c_i][z_i] and neighbors[True] == 3:
                    new_data[r_i][c_i][z_i] = True
                else:
                    new_data[r_i][c_i][z_i] = False
    return new_data


def run_n_cycles_3d(data: List[List[List[bool]]], n: int = 6):
    """Run n cycles, make sure to resize the data"""
    # somehow after the first iteration only one dim gets bigger...
    new_data = data
    for i in range(n):
        # every dimension has to become bigger by one
        bigger_data = deepcopy(new_data)
        for r_i, row in enumerate(bigger_data):
            for c_i, col in enumerate(row):
                col.insert(len(col), False)
                col.insert(0, False)
            add_row = [False for i in range(len(row[r_i]))]
            row.insert(len(row), deepcopy(add_row))
            row.insert(0, deepcopy(add_row))
        add_bigger = [[False for i in range(len(bigger_data[0][0]))] for j in range(len(bigger_data[0]))]
        bigger_data.insert(len(new_data), deepcopy(add_bigger))
        bigger_data.insert(0, deepcopy(add_bigger))
        # calculate new state
        new_data = run_cycle_3d(bigger_data)
    return new_data


def count_active_cubes_3d(data: List[List[List[bool]]]) -> int:
    """count every active cube"""
    return sum(sum(sum(z for z in y) for y in x) for x in data)


def run_cycle_4d(data: List[List[List[List[bool]]]]):
    """Cubes chances their state simultaneously"""
    def adjacent_neighbors(d, r, c, n, w):  # row col nested
        """calculate the types of adjacent seats"""
        seeing_types = {True: 0, False: 0}
        # for every 4D neighbor
        for dire in directions_4d:
            neigh_val = get_neighbor_in_direction(d, (r, c, n, w), dire)
            if not (neigh_val is None):
                seeing_types[neigh_val] += 1
        return seeing_types

    def get_neighbor_in_direction(d, pos: Tuple[int, int, int, int], direction: Tuple[int, int, int, int]) -> bool:
        """get the neighboring element in the direction"""
        i, j, k, l = tuple_add_tuple(pos, direction)
        return d[i][j][k][l] if 0 <= i < len(d) and 0 <= j < len(d[i]) and 0 <= k < len(d[i][j]) and 0 <= l < len(d[i][j][k]) else None

    # calculate new active states
    new_data = deepcopy(data)
    for r_i, row in enumerate(new_data):
        for c_i, col in enumerate(row):
            for z_i, nested in enumerate(col):
                for w_i, weights in enumerate(nested):
                    # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive. If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes
                    # active. Otherwise, the cube remains inactive.
                    neighbors = adjacent_neighbors(data, r_i, c_i, z_i, w_i)
                    if data[r_i][c_i][z_i][w_i] and 2 <= neighbors[True] <= 3:
                        new_data[r_i][c_i][z_i][w_i] = True
                    elif not data[r_i][c_i][z_i][w_i] and neighbors[True] == 3:
                        new_data[r_i][c_i][z_i][w_i] = True
                    else:
                        new_data[r_i][c_i][z_i][w_i] = False
    return new_data


def run_n_cycles_4d(data: List[List[List[List[bool]]]], n: int = 6):
    """Run n cycles, make sure to resize the data"""
    # somehow after the first iteration only one dim gets bigger...
    new_data = data
    for i in range(n):
        # every dimension has to become bigger by one
        bigger_data: List[List[List[List[bool]]]]
        bigger_data = deepcopy(new_data)
        for w_i, weight in enumerate(bigger_data):
            for r_i, row in enumerate(weight):
                for c_i, col in enumerate(row):
                    col.insert(len(col), False)
                    col.insert(0, False)
                add_r = [False for i in range(len(row[0]))]
                row.insert(len(row), deepcopy(add_r))
                row.insert(0, deepcopy(add_r))
            add_z = [[False for i in range(len(weight[0][0]))] for j in range(len(weight[0]))]
            weight.insert(len(new_data), deepcopy(add_z))
            weight.insert(0, deepcopy(add_z))
        add_w = [[[False for h in range(len(bigger_data[0][0][0]))] for i in range(len(bigger_data[0][0]))] for j in range(len(bigger_data[0]))]
        bigger_data.insert(len(new_data), deepcopy(add_w))
        bigger_data.insert(0, deepcopy(add_w))

        # calculate new state
        new_data = run_cycle_4d(bigger_data)
    return new_data


def count_active_cubes_4d(data: List[List[List[List[bool]]]]) -> int:
    """count every active cube"""
    return sum(sum(sum(sum(a for a in z) for z in y) for y in x) for x in data)


class Test2020Day17(unittest.TestCase):
    def test_simple_count_cube(self):
        self.assertEqual(count_active_cubes_3d(symbols_to_bool([".#.", "..#", "###"], dim=3)), 5)
        self.assertEqual(count_active_cubes_4d(symbols_to_bool([".#.", "..#", "###"], dim=4)), 5)

    def test_count_after_nth_cycle_3d(self):
        for n, nof_cubes in [
            [1, 11],
            [2, 21],
            [3, 38],
            [6, 112],
        ]:
            with self.subTest(msg=""):
                data = symbols_to_bool([".#.", "..#", "###"], dim=3)
                self.assertEqual(nof_cubes, count_active_cubes_3d(run_n_cycles_3d(data, n)))

    def test_count_after_nth_cycle_4d(self):
        for n, nof_cubes in [
            [1, 29],
            [2, 60],
            # [6, 848],
        ]:
            with self.subTest(msg=""):
                data = symbols_to_bool([".#.", "..#", "###"], dim=4)
                self.assertEqual(nof_cubes, count_active_cubes_4d(run_n_cycles_4d(data, n)))



if __name__ == '__main__':
    print(">>> Start Main 17:")
    puzzle_input = [
        "..##.##.",
        "#.#..###",
        "##.#.#.#",
        "#.#.##.#",
        "###..#..",
        ".#.#..##",
        "#.##.###",
        "#.#..##."
    ]
    puzzle_input_bool_3d = symbols_to_bool(puzzle_input, dim=3)
    print("Part 1):")
    print(count_active_cubes_3d(run_n_cycles_3d(deepcopy(puzzle_input_bool_3d))))
    print("Part 2):")
    puzzle_input_bool_4d = symbols_to_bool(puzzle_input, dim=4)
    print(count_active_cubes_4d(run_n_cycles_4d(deepcopy(puzzle_input_bool_4d))))
    print("End Main 17<<<")
