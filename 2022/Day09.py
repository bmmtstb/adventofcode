import unittest
from typing import Dict, List, Tuple, Set

import numpy as np

from helper.file import read_lines_as_list

# set up types
Position = np.ndarray
Motion = Tuple[str, int]
Motions = List[Motion]

directions: Dict[str, np.ndarray] = {
    "U": np.array([-1, 0]),
    "D": np.array([1, 0]),
    "L": np.array([0, -1]),
    "R": np.array([0, 1]),
}


def move_rope(head_pos: Position, tail_pos: Position) -> Tuple[Position, Position]:
    """given an initial configuration, move the head and potentially the tail, return new positions"""
    head_tail_distance = head_pos - tail_pos
    # tail does not need to be moved if it touches the head
    if np.all(np.abs(head_tail_distance) <= 1):
        return head_pos, tail_pos
    # tail needs to be moved
    tail_pos += np.sign(head_tail_distance)
    return head_pos, tail_pos


def follow_motions(motions: Motions, knots: int = 2) -> int:
    """
    let the rope follow a given list of commands
    rope has length of knots
    return number of unique positions visited by the tail
    """
    rope_pos: List[Position] = [np.zeros(2).copy() for _ in range(knots)]
    tail_visited_positions: List[Position] = [np.zeros(2)]
    for motion in motions:
        # get direction and distance from motion
        direction, distance = motion
        distance = int(distance)
        for _ in range(distance):
            # change position of head
            rope_pos[0] += directions[direction]

            # for every knot head - tail combination
            for head_i in range(knots - 1):
                rope_pos[head_i], rope_pos[head_i + 1] = move_rope(
                    head_pos=rope_pos[head_i], tail_pos=rope_pos[head_i + 1]
                )

            # add position of tail
            tail_visited_positions.append(rope_pos[-1].copy())
    return len(np.unique(np.array(tail_visited_positions), axis=0))


class Test2022Day09(unittest.TestCase):
    test_motions: Motions = [
        ("R", "4"),
        ("U", "4"),
        ("L", "3"),
        ("D", "1"),
        ("R", "4"),
        ("D", "1"),
        ("L", "5"),
        ("R", "2"),
    ]
    test_motions_2: Motions = [
        ("R", "5"),
        ("U", "8"),
        ("L", "8"),
        ("D", "3"),
        ("R", "17"),
        ("D", "10"),
        ("L", "25"),
        ("U", "20"),
    ]

    def test_move_rope(self):
        for tail_pos, head_pos, new_tail_pos in [
            ((0, 0), (0, 1), (0, 0)),  # initial step
            ((1, 1), (1, 3), (1, 2)),
            ((1, 1), (3, 1), (2, 1)),
            ((3, 1), (1, 2), (2, 2)),  # diagonal step
            ((3, 1), (2, 3), (2, 2)),  # diagonal step
        ]:
            with self.subTest(
                msg=f"tail_pos: {tail_pos}, head_pos: {head_pos}, new_tail_pos: {new_tail_pos}"
            ):
                nhp, ntp = move_rope(
                    head_pos=np.array(head_pos), tail_pos=np.array(tail_pos)
                )
                self.assertTrue(np.alltrue(nhp == np.array(head_pos)))
                self.assertTrue(np.alltrue(ntp == np.array(new_tail_pos)))

    def test_follow_motions_length(self):
        for motions, knots, visited in [
            (self.test_motions, 2, 13),
            (self.test_motions, 10, 1),
            (self.test_motions_2, 10, 36),
        ]:
            with self.subTest(msg=f"knots: {knots}, visited: {visited}"):
                self.assertEqual(follow_motions(motions=motions, knots=knots), visited)


if __name__ == "__main__":
    print(">>> Start Main 09:")
    puzzle_input = read_lines_as_list("data/09.txt", split=" ")
    print("Part 1): ", follow_motions(puzzle_input, knots=2))
    print("Part 2): ", follow_motions(puzzle_input, knots=10))
    print("End Main 09<<<")
