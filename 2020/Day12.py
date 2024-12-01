import unittest
from typing import List, Tuple
from helper.tuple import tuple_mult_scalar, tuple_add_tuple

puzzle_input = []


def load(filepath: str) -> List[Tuple[str, int]]:
    """load a test file into correct format"""
    data = []
    with open(filepath) as file:
        for l in file.readlines():
            data.append((str(l[0]), int(l[1:].replace("\n", ""))))
    return data


# Action N means to move north by the given value.
# Action S means to move south by the given value.
# Action E means to move east by the given value.
# Action W means to move west by the given value.
# Action L means to turn left the given number of degrees.
# Action R means to turn right the given number of degrees.
# Action F means to move forward by the given value in the direction the ship is currently facing.


class Ship:
    """create a simple Ship and steer it according to directions, maybe using a waypoint"""

    def __init__(
        self,
        pos: Tuple[int, int] = (0, 0),
        waypoint_exists: bool = False,
        wp_pos: Tuple[int, int] = (10, 1),
    ):
        self.facing: Tuple[int, int] = (1, 0)  # (x, y) east
        self.pos: Tuple[int, int] = pos  # (x, y)
        self.has_wp: bool = waypoint_exists
        self.wp: Tuple[int, int] = wp_pos

    def move_ship(self, dist: Tuple[int, int]):
        """move ship in the given direction"""
        self.pos = tuple_add_tuple(self.pos, dist)

    def move_wp(self, dist: Tuple[int, int]):
        """move the waypoint in a given direction"""
        self.wp = tuple_add_tuple(self.wp, dist)

    def turn_ship(self, direction: str, deg: int):
        """move in the given direction"""
        if deg == 180:
            self.facing = tuple_mult_scalar(self.facing, -1)
        elif deg == 360 or deg == 0:
            return
        elif (deg == 90 and direction == "R") or (deg == 270 and direction == "L"):
            self.facing = (self.facing[1], -self.facing[0])
        elif (deg == 90 and direction == "L") or (deg == 270 and direction == "R"):
            self.facing = (-self.facing[1], self.facing[0])
        else:
            raise Exception(
                "turn value of {} not expected for turn, aborting".format(deg)
            )

    def turn_waypoint(self, direction: str, deg: int):
        """turn the waypoint around the ship"""
        if deg == 180:
            self.wp = tuple_mult_scalar(self.wp, -1)
        elif deg == 360 or deg == 0:
            return
        elif (deg == 90 and direction == "R") or (deg == 270 and direction == "L"):
            self.wp = (self.wp[1], -self.wp[0])
        elif (deg == 90 and direction == "L") or (deg == 270 and direction == "R"):
            self.wp = (-self.wp[1], self.wp[0])
        else:
            raise Exception(
                "turn value of {} not expected for turn_waypoint, aborting".format(deg)
            )

    def follow_directions(self, instructions: List[Tuple[str, int]]):
        """follow a given list of instructions"""
        for instruction in instructions:
            act, value = instruction
            if act == "L" or act == "R":
                if self.has_wp:
                    self.turn_waypoint(act, value)
                else:
                    self.turn_ship(act, value)
            elif act == "F":
                if self.has_wp:
                    self.move_ship(tuple_mult_scalar(self.wp, value))
                else:
                    self.move_ship(tuple_mult_scalar(self.facing, value))
            elif act == "N":
                if self.has_wp:
                    self.move_wp(tuple_mult_scalar((0, 1), value))
                else:
                    self.move_ship(tuple_mult_scalar((0, 1), value))
            elif act == "E":
                if self.has_wp:
                    self.move_wp(tuple_mult_scalar((1, 0), value))
                else:
                    self.move_ship(tuple_mult_scalar((1, 0), value))
            elif act == "S":
                if self.has_wp:
                    self.move_wp(tuple_mult_scalar((0, -1), value))
                else:
                    self.move_ship(tuple_mult_scalar((0, -1), value))
            elif act == "W":
                if self.has_wp:
                    self.move_wp(tuple_mult_scalar((-1, 0), value))
                else:
                    self.move_ship(tuple_mult_scalar((-1, 0), value))
            else:
                raise Exception("Invalid instruction {}".format(act))

    def get_manhatten_distance(self):
        """calculate manhatten distance as sum of two position values"""
        return sum(map(lambda a: abs(a), self.pos))


class Test2020Day12(unittest.TestCase):
    def test_ship(self):
        for directs, fin_pos, man_dist in [
            [[("F", 10)], (10, 0), 10],
            [[("F", 10), ("N", 3)], (10, 3), 13],
            [[("F", 10), ("N", 3), ("F", 7)], (17, 3), 20],
            [[("F", 10), ("N", 3), ("F", 7), ("R", 90)], (17, 3), 20],
            [[("F", 10), ("N", 3), ("F", 7), ("R", 90), ("F", 11)], (17, -8), 25],
        ]:
            with self.subTest():
                test_ship = Ship()
                test_ship.follow_directions(directs)
                self.assertTupleEqual(test_ship.pos, fin_pos)
                self.assertEqual(test_ship.get_manhatten_distance(), man_dist)

    def test_waypoint(self):
        for directs, fin_pos, wp_pos, man_dist in [
            [[("F", 10)], (100, 10), (10, 1), 110],
            [[("F", 10), ("N", 3)], (100, 10), (10, 4), 110],
            [[("F", 10), ("N", 3), ("F", 7)], (170, 38), (10, 4), 208],
            [[("F", 10), ("N", 3), ("F", 7), ("R", 90)], (170, 38), (4, -10), 208],
            [
                [("F", 10), ("N", 3), ("F", 7), ("R", 90), ("F", 11)],
                (214, -72),
                (4, -10),
                286,
            ],
        ]:
            with self.subTest():
                test_ship = Ship(waypoint_exists=True)
                test_ship.follow_directions(directs)
                self.assertTupleEqual(test_ship.pos, fin_pos)
                self.assertTupleEqual(test_ship.wp, wp_pos)
                self.assertEqual(test_ship.get_manhatten_distance(), man_dist)


if __name__ == "__main__":
    print(">>> Start Main 12:")
    ship = Ship()
    dirs = load("data/12.txt")
    print("Part 1):")
    ship.follow_directions(dirs)
    print(ship.get_manhatten_distance())
    print("Part 2):")
    ship_wp = Ship(waypoint_exists=True)
    ship_wp.follow_directions(dirs)
    print(ship_wp.get_manhatten_distance())
    print("End Main 12<<<")
