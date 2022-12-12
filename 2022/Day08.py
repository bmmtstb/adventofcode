import unittest
from typing import Dict, List, Tuple, Set

import numpy as np

from helper.file import read_lines_as_list


def get_visible_indices(tree_line: np.ndarray) -> List[int]:
    """from a line of trees get the indices of every tree that is visible, always from start to end of list"""
    visible = []
    max_height = -1

    for tree_idx, tree in enumerate(tree_line):
        if tree > max_height:
            visible.append(tree_idx)
            max_height = tree
    return visible


def get_outside_visible_count(forest: np.ndarray) -> int:
    """get the count of trees visible from outside"""
    height, width = forest.shape
    # add border
    visible_indices: Set[Tuple[int, int]] = set(
        [(0, i) for i in range(width)] +
        [(height - 1, i) for i in range(width)] +
        [(j, 0) for j in range(height)] +
        [(j, width - 1) for j in range(height)]
    )
    # left to right and right to left
    # does not have to analyze first nor last row, they have been added either way
    for tree_line_id, tree_line in enumerate(forest[1:-1], start=1):
        # l to r
        visible_tree_indices = get_visible_indices(tree_line)
        visible_indices.update(set((tree_line_id, tree_id) for tree_id in visible_tree_indices))
        # r to l
        visible_tree_indices = get_visible_indices(tree_line[::-1])
        visible_indices.update(set((tree_line_id, width - 1 - tree_id) for tree_id in visible_tree_indices))

    # top to bottom and bottom to top
    # does not have to analyze first nor last row, they have been added either way
    for tree_line_id in range(1, height - 1):
        # top to bottom
        visible_tree_indices = get_visible_indices(forest[:, tree_line_id])
        visible_indices.update(set((tree_id, tree_line_id) for tree_id in visible_tree_indices))
        # bottom to top
        visible_tree_indices = get_visible_indices(forest[::-1, tree_line_id])
        visible_indices.update(set((height - 1 - tree_id, tree_line_id) for tree_id in visible_tree_indices))

    return len(visible_indices)


def get_lower_than(tree_line: np.ndarray, height: int) -> int:
    """given a list of tree heights, check how many of them are lower than height, stop on the border"""
    lower: int = 0
    for tree in tree_line:
        if tree < height:
            lower += 1
        else:
            return lower + 1
    return lower


def get_position_scenic_score(forest: np.ndarray, position: Tuple[int, int]) -> int:
    """given a position in the forest, calculate the scenic score"""
    forest_height, forest_width = forest.shape
    self_height = forest[position]
    up = get_lower_than(forest[position[0], :position[1]][::-1], height=self_height)
    down = get_lower_than(forest[position[0], position[1]+1:forest_height], height=self_height)
    left = get_lower_than(forest[:position[0]:, position[1]][::-1], height=self_height)
    right = get_lower_than(forest[position[0]+1:forest_width, position[1]], height=self_height)
    return up * down * left * right


def get_max_scenic_score(forest: np.ndarray) -> int:
    """given a forest calculate the scenic score for all non-border tiles and return the maximum"""
    max_score = 0
    height, width = forest.shape
    # border has 0 - value -> ignore it
    for w in range(1, width - 1):
        for h in range(1, height - 1):
            score = get_position_scenic_score(forest, (h, w))
            max_score = max(max_score, score)
    return max_score


class Test2022Day08(unittest.TestCase):
    test_area_values = np.array([
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ])
    pyramid_trees = np.array([
        [1, 2, 3, 2, 1],
        [2, 3, 4, 3, 2],
        [3, 4, 5, 4, 3],
        [2, 3, 4, 3, 2],
        [1, 2, 3, 2, 1],
    ])

    def test_load_data(self):
        # dummy check
        self.assertTrue(
            np.alltrue(
                np.array(read_lines_as_list(filepath="data/08-test.txt", instance_type=int, split="every")) == \
                self.test_area_values
            ))

    def test_get_visible_indices(self):
        for tree_list, visible_trees in [
            (self.test_area_values[0], [0, 3]),
            (self.test_area_values[1], [0, 1]),
            (self.test_area_values[2], [0]),
            (self.test_area_values[3], [0, 2, 4]),
            (self.test_area_values[4], [0, 1, 3]),
            (self.test_area_values[0, ::-1], [0, 1]),
            (self.test_area_values[1, ::-1], [0, 2]),
            (self.test_area_values[2, ::-1], [0, 1, 3, 4]),
            (self.test_area_values[3, ::-1], [0]),
            (self.test_area_values[4, ::-1], [0, 1]),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8]),
            ([1, 1, 1, 1], [0]),
        ]:
            with self.subTest(msg=f'tree list: {tree_list}'):
                self.assertEqual(get_visible_indices(tree_list), visible_trees)

    def test_get_lower_than(self):
        for tree_list, self_height, amount_visible in [
            (self.test_area_values[0], 5, 4),
            (self.test_area_values[1], 5, 2),
            (self.test_area_values[2], 5, 1),
            (self.test_area_values[3], 5, 3),
            (self.test_area_values[4], 5, 2),
            (self.test_area_values[0], 1, 1),
        ]:
            with self.subTest(msg=f'tree list: {tree_list}, height: {self_height}'):
                self.assertEqual(get_lower_than(tree_list, self_height), amount_visible)

    def test_get_position_scenic_score(self):
        for forest, position, score in [
            (self.test_area_values, (0, 1), 0),
            (self.test_area_values, (1, 2), 4),
            (self.test_area_values, (3, 2), 8),
            (self.pyramid_trees, (2, 2), 16),
        ]:
            with self.subTest(msg=f'pos: {position}, score: {score}'):
                self.assertEqual(get_position_scenic_score(forest, position), score)

    def test_get_outside_visible_count(self):
        for area, count in [
            (self.test_area_values, 21),
            (np.rot90(self.test_area_values), 21),
            (self.pyramid_trees, 25),
            (np.array(read_lines_as_list(filepath="data/08.txt", instance_type=int, split="every")), 1733),
        ]:
            with self.subTest(msg=f'count: {count}'):
                self.assertEqual(get_outside_visible_count(area), count)

    def test_get_max_scenic_score(self):
        for forest, max_score in [
            (self.test_area_values, 8),
            (self.pyramid_trees, 16),
        ]:
            with self.subTest(msg=f'max: {max_score}'):
                self.assertEqual(get_max_scenic_score(forest), max_score)


if __name__ == '__main__':
    print(">>> Start Main 08:")
    puzzle_input = np.array(read_lines_as_list(filepath="data/08.txt", instance_type=int, split="every"))
    print("Part 1): ", get_outside_visible_count(puzzle_input))
    print("Part 2): ", get_max_scenic_score(puzzle_input))
    print("End Main 08<<<")
