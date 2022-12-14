import unittest
from copy import deepcopy
from typing import Dict, List, Tuple, Set

import numpy as np

from helper.file import read_lines_as_list
from helper.tuple import tuple_add_tuple

# x represents distance to the right
# y represents distance down

Position = Tuple[int, int]
Path = List[Position]
Paths = List[Path]
Cave = np.ndarray


class CaveSystem:
    """Cave system for day 14"""

    def __init__(self, paths: Paths, sand_point: Position = (500, 0), abyss_width: int = 0):
        """
        paths: a list of paths
        sand_point: position the sand exits
        abyss_width: iff > 0 there is a floor 2 beneath the lowest point -> guess how large this should be
        """
        self.abyss_width: int = abyss_width
        height_mod = 0 if self.abyss_width == 0 else 2
        # get min and max in paths in all directions, make sure to include sand spawn position
        self.min_x: int = min(min(min(pos[0] for pos in path) for path in paths), sand_point[0]) - self.abyss_width
        self.max_x: int = max(max(max(pos[0] for pos in path) for path in paths), sand_point[0]) + self.abyss_width
        self.min_y: int = min(min(min(pos[1] for pos in path) for path in paths), sand_point[1])
        self.max_y: int = max(max(max(pos[1] for pos in path) for path in paths), sand_point[1]) + height_mod
        self.width: int = self.max_x - self.min_x + 1
        self.height: int = self.max_y - self.min_y + 1
        # create rock cave-system
        # 2 = rock, 1 = sand, 0 = air
        self.cave_system_map: Cave = self.creat_cave_system_map_from_paths(paths=paths)
        # set up sand
        self.sand_spawn: Position = (sand_point[1] - self.min_y, sand_point[0] - self.min_x)
        self.sand_amount: int = 0

    def creat_cave_system_map_from_paths(self, paths: Paths) -> Cave:
        """create cave system map from paths"""
        cave_map = np.zeros((self.height, self.width), dtype=int)
        # add "floor"
        if self.abyss_width > 0:
            cave_map[-1, :] = 2
        # add cave walls from scanner values (paths)
        for path in paths:
            if len(path) <= 1:
                raise Exception("path should at least have two values")
            # connect two paths
            for i_pos in range(len(path) - 1):
                y_start, y_end = path[i_pos][1] - self.min_y, path[i_pos + 1][1] - self.min_y
                x_start, x_end = path[i_pos][0] - self.min_x, path[i_pos + 1][0] - self.min_x
                if x_start != x_end and y_start != y_end:
                    raise Exception("Path should only move in one direction, moved in two")
                # replace current values in map with values for border
                cave_map[
                min(y_start, y_end):max(y_start, y_end) + 1,
                min(x_start, x_end):max(x_start, x_end) + 1
                ] = 2
        return cave_map

    def produce_and_move_sand(self) -> bool:
        """
        produce one new sand tile, and find its final position given the current map of the cave system
        returns True if sand was places, False if it fell to the abyss
        """
        # "spawn" new sand
        sand_pos: Position = deepcopy(self.sand_spawn)
        old_pos: Position = tuple()
        # A unit of sand always falls down one step if possible.
        # If the tile immediately below is blocked (by rock or sand), the unit of sand attempts to instead move
        # diagonally one step down and to the left. If that tile is blocked, the unit of sand attempts to instead move
        # diagonally one step down and to the right. Sand keeps moving as long as it is able to do so, at each step
        # trying to move down, then down-left, then down-right.
        steps = [(1, 0), (1, -1), (1, 1)]
        while old_pos != sand_pos:
            for possible_step in steps:
                old_pos = sand_pos
                next_pos: Position = tuple_add_tuple(sand_pos, possible_step)
                # found abyss, return
                if next_pos[0] >= self.height or \
                        next_pos[1] < 0 or \
                        next_pos[1] >= self.width:
                    return False
                # skip possibility if cave_map has sth else than air
                elif self.cave_system_map[next_pos] > 0:
                    continue
                # possible next position found, break for loop
                else:
                    sand_pos = next_pos
                    break

        # If all three possible destinations are blocked, the unit of sand comes to rest and can be counted
        self.cave_system_map[sand_pos] = 1
        self.sand_amount += 1
        # return false if the sand stays on the source field
        if sand_pos == self.sand_spawn:
            return False
        # the unit sand did find a regular place
        return True

    def produce_sand_till_end(self) -> int:
        """keep producing sand until the first grain falls into the abyss or the sand source is blocked"""
        while self.produce_and_move_sand():
            pass
        return self.sand_amount


class Test2022Day14(unittest.TestCase):
    test_paths: Paths = read_lines_as_list(
        "data/14-test.txt",
        instance_type=lambda pos: tuple(int(x) for x in pos.split(",")),
        split=" -> "
    )
    test_cave_system = CaveSystem(paths=deepcopy(test_paths))
    test_cave_system_no_abyss = CaveSystem(paths=deepcopy(test_paths), abyss_width=9)

    before_with_abyss = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 2, 0, 0, 0, 2, 2], [0, 0, 0, 0, 2, 0, 0, 0, 2, 0],
                                  [0, 0, 2, 2, 2, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 2, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2, 0]])

    before_without_abyss = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                     [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]])

    after_with_abyss = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                                 [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]])

    after1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 2, 0, 0, 0, 2, 2], [0, 0, 0, 0, 2, 0, 0, 0, 2, 0],
                       [0, 0, 2, 2, 2, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
                       [0, 0, 0, 0, 0, 0, 1, 0, 2, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2, 0]])

    after2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 2, 0, 0, 0, 2, 2], [0, 0, 0, 0, 2, 0, 0, 0, 2, 0],
                       [0, 0, 2, 2, 2, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
                       [0, 0, 0, 0, 0, 1, 1, 0, 2, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2, 0]])

    after5 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 2, 0, 0, 0, 2, 2], [0, 0, 0, 0, 2, 0, 0, 0, 2, 0],
                       [0, 0, 2, 2, 2, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 1, 0, 2, 0],
                       [0, 0, 0, 0, 1, 1, 1, 1, 2, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2, 0]])

    after22 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 2, 1, 1, 1, 2, 2], [0, 0, 0, 0, 2, 1, 1, 1, 2, 0],
                        [0, 0, 2, 2, 2, 1, 1, 1, 2, 0], [0, 0, 0, 0, 1, 1, 1, 1, 2, 0],
                        [0, 0, 0, 1, 1, 1, 1, 1, 2, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2, 0]])

    after24 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 2, 1, 1, 1, 2, 2], [0, 0, 0, 1, 2, 1, 1, 1, 2, 0],
                        [0, 0, 2, 2, 2, 1, 1, 1, 2, 0], [0, 0, 0, 0, 1, 1, 1, 1, 2, 0],
                        [0, 1, 0, 1, 1, 1, 1, 1, 2, 0], [2, 2, 2, 2, 2, 2, 2, 2, 2, 0]])

    def test_cave_generation(self):
        self.assertTrue(np.alltrue(self.test_cave_system.cave_system_map == self.before_with_abyss))

    def test_falling_sand_stepwise(self):
        done_iterations: int = 0
        cave_system = deepcopy(self.test_cave_system)

        for cave_map, iteration in [
            (self.after1, 1),
            (self.after2, 2),
            (self.after5, 5),
            (self.after22, 22),
            (self.after24, 24),
        ]:
            with self.subTest(msg=f'iteration {iteration}'):
                # use one cave system object and simulate all cases back to back, keep track of iterations
                for _ in range(iteration - done_iterations):
                    cave_system.produce_and_move_sand()
                done_iterations = iteration
                self.assertTrue(np.alltrue(cave_map == cave_system.cave_system_map))

    def test_fail_to_abyss(self):
        self.assertEqual(deepcopy(self.test_cave_system).produce_sand_till_end(), 24)

    def test_map_with_floor_before(self):
        cave_system = deepcopy(self.test_cave_system_no_abyss)
        self.assertTrue(np.alltrue(
            cave_system.cave_system_map == self.before_without_abyss
        ))

    def test_map_with_floor_after(self):
        cave_system = deepcopy(self.test_cave_system_no_abyss)
        for _ in range(92):
            cave_system.produce_and_move_sand()
        self.assertTrue(np.alltrue(
            cave_system.cave_system_map == self.after_with_abyss
        ))


    def test_fail_no_abyss(self):
        self.assertEqual(deepcopy(self.test_cave_system_no_abyss).produce_sand_till_end(), 93)


if __name__ == '__main__':
    print(">>> Start Main 14:")
    puzzle_input: Paths = read_lines_as_list(
        "data/14.txt",
        instance_type=lambda pos: tuple(int(x) for x in pos.split(",")),
        split=" -> "
    )
    print("Part 1): ", CaveSystem(paths=deepcopy(puzzle_input)).produce_sand_till_end())
    print("Part 2): ", CaveSystem(paths=deepcopy(puzzle_input), abyss_width=300).produce_sand_till_end())
    print("End Main 14<<<")
