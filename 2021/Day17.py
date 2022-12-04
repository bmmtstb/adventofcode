import unittest
from typing import Dict, List, Tuple, Set

from helper.tuple import tuple_add_tuple


Position = Tuple[int, int]
Velocity = Tuple[int, int]
TargetAreaBorders = Tuple[Tuple[int, int], Tuple[int, int]]


def probe_step(pos: Position, vel: Velocity) -> (Position, Velocity):
    """given all the params, calculate the next step"""
    new_pos = tuple_add_tuple(pos, vel)
    new_vel = (vel[0] + (- 1 if vel[0] > 0 else 0 if vel[0] == 0 else 1), vel[1] - 1)
    return new_pos, new_vel


def probe_hits_target(init_vel: Velocity, target_area: TargetAreaBorders, init_pos: Position = (0, 0)) -> (bool, int):
    """Check if a probe hits the given target area"""
    target_x_range = range(target_area[0][0], target_area[0][1] + 1 if target_area[0][1] > target_area[0][0] else -1, 1 if target_area[0][1] > target_area[0][0] else -1)
    target_y_range = range(target_area[1][0], target_area[1][1] + 1 if target_area[1][1] > target_area[1][0] else -1, 1 if target_area[1][1] > target_area[1][0] else -1)

    curr_pos: Position = init_pos
    curr_vel: Velocity = init_vel
    curr_step = 0

    highest_y: int = curr_pos[1]

    while True:
        # check for hit
        if curr_pos[0] in target_x_range and curr_pos[1] in target_y_range:
            return True, highest_y

        # step forward
        curr_pos, curr_vel = probe_step(curr_pos, curr_vel)
        curr_step += 1

        # update highest
        if curr_pos[1] > highest_y:
            highest_y = curr_pos[1]

        # break if target is unreachable
        if curr_vel[0] == 0 and curr_pos[0] not in target_x_range:
            # x vel is 0 and not in x target area
            break
        elif curr_vel[1] < 0 and curr_pos[1] < target_area[1][0]:
            # y vel is negative and pos is below target
            break
        elif curr_vel[0] > 0 and curr_pos[0] > target_area[0][1]:
            # x is greater than range and x_vel is > 0
            break
    return False, highest_y


def find_max_height(target_area: TargetAreaBorders, init_pos: Position = (0, 0)) -> (Velocity, int):
    """find the highest y value while hitting the target from a given starting position"""
    highest = 0
    highest_vel: Velocity = (0, 0)
    velocities = [(vx, vy) for vx in range(1, int(0.5 * target_area[0][1] + 1)) for vy in range(-abs(target_area[1][0]), target_area[0][1] + 1)]
    for vel in velocities:
        hits, h_y = probe_hits_target(vel, target_area, init_pos)
        if hits and h_y > highest:
            highest = h_y
            highest_vel = vel
    return highest_vel, highest


def find_every_possible_velocity(target_area: TargetAreaBorders, init_pos: Position = (0, 0)) -> List[Velocity]:
    """st"""
    possible_vels: List[Velocity] = []
    velocities = [(vx, vy) for vx in range(1, target_area[0][1] + 1) for vy in
                  range(-abs(target_area[1][0]), target_area[0][1] + 1)]
    for vel in velocities:
        hits, _ = probe_hits_target(vel, target_area, init_pos)
        if hits:
            possible_vels.append(vel)
    return possible_vels


class Test2021Day17(unittest.TestCase):
    test_area: TargetAreaBorders = ((20, 30), (-10, -5))
    puzzle_area: TargetAreaBorders = ((150, 193), (-136, -86))

    def test_hits_target(self):
        for vel, hits, highest in [
            [(7, 2), True, 3],
            [(6, 3), True, 6],
            [(9, 0), True, 0],
            [(17, -4), False, 0],
            [(6, 9), True, 45],
        ]:
            with self.subTest():
                c_hit, c_highest = probe_hits_target(vel, self.test_area)
                self.assertEqual(c_hit, hits)
                self.assertEqual(c_highest, highest)

    def test_find_max_height(self):
        perfect_vel = (6, 9)
        perfect_height = 45
        h_vel, h_y = find_max_height(self.test_area)
        self.assertEqual(h_vel, perfect_vel)
        self.assertEqual(h_y, perfect_height)

    def test_find_all_possible(self):
        self.assertEqual(len(find_every_possible_velocity(self.test_area)), 112)
        self.assertEqual(len(find_every_possible_velocity(self.puzzle_area)), 3767)


if __name__ == '__main__':
    print(">>> Start Main 17:")
    puzzle_str = "target area: x = 150..193, y = -136..-86"
    puzzle_target = ((150, 193), (-136, -86))
    print("Part 1): ", find_max_height(puzzle_target))
    print("Part 2): ", len(find_every_possible_velocity(puzzle_target)))  # 3075
    print("End Main 17<<<")
