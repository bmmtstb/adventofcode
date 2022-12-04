import unittest
from copy import deepcopy
from typing import Dict, List, Tuple, Set

from helper.file import load_file_and_split


Positions = Set[Tuple[int, int]]


def fold_along_axis(positions: Positions, axis: int, axis_pos: int):
    """Fold the paper left or up along given axis"""
    # there may not be any points on the line
    if any(pos[axis] == axis_pos for pos in positions):
        raise Exception("No folds along axis with values!")
    removed: Positions = set()
    added: Positions = set()
    for pos in positions:
        if pos[axis] > axis_pos:
            new_pos: Tuple[int, int]
            if axis == 0:
                new_pos = (2 * axis_pos - pos[0], pos[1])

            elif axis == 1:
                new_pos = (pos[0], 2 * axis_pos - pos[1])
            else:
                raise Exception("Invalid axis {}".format(axis))
            added.add(new_pos)
            removed.add(pos)
    for rem in removed:
        positions.remove(rem)
    for add in added:
        positions.add(add)


def draw_positions(positions: Set[Tuple[int, int]], console_print: bool = False) -> List[str]:
    """draw a "#" for every position, "." otherwise"""
    min_x: int = min(pos[0] for pos in positions)
    max_x: int = max(pos[0] for pos in positions)
    min_y: int = min(pos[1] for pos in positions)
    max_y: int = max(pos[1] for pos in positions)

    picture = ["".join("#" if (x, y) in positions else "." for x in range(min_x, max_x + 1)) for y in range(min_y, max_y + 1)]
    if console_print:
        for p in picture:
            print(p)
    return picture


def fold_paper(positions: Positions, folds: List[str]) -> Positions:
    """fold the transparent along the given folds"""
    for fold in folds:
        if fold.startswith("y"):
            fold_along_axis(positions, 1, int(fold[2:]))
        elif fold.startswith("x"):
            fold_along_axis(positions, 0, int(fold[2:]))
        else:
            raise Exception("Fold along axis {} not defined".format(fold))
    return positions


class Test2021Day13(unittest.TestCase):
    test_dots = {(6, 10), (0, 14), (9, 10), (0, 3), (10, 4), (4, 11), (6, 0), (6, 12), (4, 1), (0, 13), (10, 12),
                 (3, 4), (3, 0), (8, 4), (1, 10), (2, 14), (8, 10), (9, 0)}

    def test_fold_nof_points(self):
        for folds, nof_points in [
            [["y=7"], 17],
            [["y=7", "x=5"], 16],
        ]:
            with self.subTest():
                self.assertEqual(len(fold_paper(deepcopy(self.test_dots), folds)), nof_points)

    def test_fold_result_visually(self):
        new_positions = fold_paper(deepcopy(self.test_dots), ["y=7", "x=5"])
        draw_str = draw_positions(new_positions)
        test_str = [
            "#####",
            "#...#",
            "#...#",
            "#...#",
            "#####"
        ]
        self.assertEqual(draw_str, test_str)



if __name__ == '__main__':
    d = load_file_and_split("data/13.txt", separator="\n\n")
    puzzle_positions: Positions = {(int(line.split(",")[0]), int(line.split(",")[1])) for line in d[0].split("\n")}
    puzzle_instructions = [s[11:] for s in d[1].split("\n") if len(s) > 0]
    print(">>> Start Main 13:")
    print("Part 1): ", len(fold_paper(deepcopy(puzzle_positions), deepcopy([puzzle_instructions[0]]))))
    print("Part 2): ")
    draw_positions(fold_paper(deepcopy(puzzle_positions), deepcopy(puzzle_instructions)), True)
    print("End Main 13<<<")
