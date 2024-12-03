import unittest
from typing import Dict, List, Tuple, Set

from helper.file import read_lines_as_list
from helper.tuple import manhattan_distance, tuple_add_tuple, tuple_subtract_tuple

Position = Tuple[int, int]  # x, y
Sensors = List["Sensor"]


class Sensor:
    def __init__(self, sensor_pos: Position, beacon_pos: Position):
        self.position: Position = sensor_pos
        self.beacon_position: Position = beacon_pos
        self.beacon_distance: int = int(
            manhattan_distance(self.position, self.beacon_position)
        )

    def can_be_distress_beacon(self, pos: Position) -> bool:
        """given a position, return whether a beacon can be present here for the given sensor"""
        # if self.is_beacon_here(pos):
        #     return False
        # if self.is_sensor_here(pos):
        #     return False
        return manhattan_distance(pos, self.position) > self.beacon_distance

    def position_is_in_sensor_range(self, pos: Position) -> bool:
        """return whether a given position is inside the sensor range (includes beacons and sensors)"""
        return manhattan_distance(pos, self.position) <= self.beacon_distance

    def can_not_be_distress_beacon(self, pos: Position) -> bool:
        """given a position return whether there can not be a beacon"""
        if self.is_beacon_here(pos):
            return False
        if self.is_sensor_here(pos):
            return True
        return manhattan_distance(pos, self.position) <= self.beacon_distance

    def is_sensor_here(self, pos: Position) -> bool:
        """returns whether at pos is the given sensor"""
        return self.position == pos

    def is_beacon_here(self, pos: Position) -> bool:
        """returns whether on pos is the own beacon"""
        return self.beacon_position == pos


class SensorBeaconMap:
    """given a list of sensors and nearest beacon positions"""

    # .................#.....
    # ................###.... <= target row
    # ........#......#####...
    # ..#....###....#######..
    # .#S#..##S##..####S####.
    # ..#....###....#######..
    # ........#......#####...
    # ................###....
    # .................#.....
    # .................^.....
    # .................| sensor x

    def __init__(self, sensors: Sensors):
        self.sensors: Sensors = sensors
        self.beacon_positions: Set[Position] = set(
            [sensor.beacon_position for sensor in self.sensors]
        )
        self.x_min = min(
            min(sensor.position[0] - sensor.beacon_distance, sensor.beacon_position[0])
            for sensor in self.sensors
        )
        self.x_max = max(
            max(sensor.position[0] + sensor.beacon_distance, sensor.beacon_position[0])
            for sensor in self.sensors
        )
        self.y_min = min(
            min(sensor.position[1] - sensor.beacon_distance, sensor.beacon_position[1])
            for sensor in self.sensors
        )
        self.y_max = max(
            max(sensor.position[1] + sensor.beacon_distance, sensor.beacon_position[1])
            for sensor in self.sensors
        )

    def can_be_beacon(self, pos: Position) -> bool:
        """return whether at the given position can be a beacon"""
        return all(sensor.can_be_distress_beacon(pos=pos) for sensor in self.sensors)

    def can_not_be_distress_beacon(self, pos: Position) -> bool:
        """return whether there can not be a beacon at given position"""
        return any(
            sensor.can_not_be_distress_beacon(pos=pos) for sensor in self.sensors
        )

    def is_inside_scanner_range(self, pos: Position) -> bool:
        """return whether pos is inside any sensor range"""
        return any(
            sensor.position_is_in_sensor_range(pos=pos) for sensor in self.sensors
        )

    def count_non_beacon_naive(self, y: int) -> int:
        """
        given a y value, count the amount of fields that can not contain a beacon
        brute force check every field, takes ages for larger spaces
        """
        # return sum(not self.can_be_distress_beacon((x, y)) for x in range(self.x_min, self.x_max + 1))
        return sum(
            self.can_not_be_distress_beacon((x, y))
            for x in range(self.x_min, self.x_max + 1)
        )

    def count_where_distress_isnt(self, y: int) -> int:
        """
        given a y value, count the amount of fields that can not contain the distress beacon
        moves fast to the right border of the ♦ areas of the current row
        """
        # return sum(not self.can_be_distress_beacon((x, y)) for x in range(self.x_min, self.x_max + 1))
        x = min(
            sensor.position[0] - (sensor.beacon_distance - abs(y - sensor.position[1]))
            for sensor in self.sensors
        )
        score = 0
        # remove all beacons that are exactly on this line (do not count)
        score -= sum(beacon_pos[1] == y for beacon_pos in self.beacon_positions)
        # remove all sensors that are exactly on this line (do not count)
        score -= sum(sensor.position[1] == y for sensor in self.sensors)
        dummy = ...
        # move from left to right through y-line
        while (
            x
            < max(
                sensor.position[0]
                + (sensor.beacon_distance - abs(y - sensor.position[1]))
                for sensor in self.sensors
            )
            + 1
        ):
            pos: Position = (x, y)
            for sensor in self.sensors:
                if sensor.position_is_in_sensor_range(pos=pos):
                    # skip steps
                    y_diff = abs(y - sensor.position[1])
                    # calculate the end of the beacon
                    beacon_right_side_line = sensor.position[0] + (
                        sensor.beacon_distance - y_diff
                    )
                    score += abs(beacon_right_side_line - x) + 1
                    x = beacon_right_side_line
                    break
            # go to next position no matter if skipped previous
            x += 1
        return score

    def find_distress_signal_location_naive(
        self, min_: int = 0, max_: int = 4_000_000
    ) -> Position:
        """find the location of the distress signal, can skip huge chunks that is part of single sensor"""
        for y in range(min_, max_ + 1):
            x = min_
            while x < max_ + 1:
                pos: Position = (x, y)
                covered: bool = False
                for sensor in self.sensors:
                    if sensor.can_not_be_distress_beacon(pos=pos):
                        covered = True
                        # skip steps
                        y_diff = abs(y - sensor.position[1])
                        x = sensor.position[0] + (sensor.beacon_distance - y_diff) + 1
                        break
                if not covered:
                    return pos

    def find_distress_signal_location_faster(
        self, min_: int = 0, max_: int = 4_000_000
    ) -> Position:
        """
        distress has to be on the outer edge of one or multiple of the beacons
        thanks to:
        https://www.reddit.com/r/adventofcode/comments/zmfwg1/2022_day_15_part_2_seekin_for_the_beacon/
        """
        # -> manhattan = 5
        # .....O.....
        # ....O#O....
        # ...O###O...
        # ..O#####O..
        # .O#######O.
        # O####S####O
        # .O#######O.
        # ..O#####O..
        # ...O###O...
        # ....O#O....
        # .....O.....

        # already_analyzed = set()
        for sensor in self.sensors:
            # upper triangle from l to r, then lower triangle from l to r excluding centerpieces
            possible_locations = set(
                [
                    tuple_add_tuple(
                        sensor.position, (sensor.beacon_distance + 1 - j, j)
                    )
                    for j in range(
                        -(sensor.beacon_distance + 1 + 1),
                        sensor.beacon_distance + 1 + 1,
                    )
                ]
                + [
                    tuple_add_tuple(
                        sensor.position, (-(sensor.beacon_distance + 1) + j, j)
                    )
                    for j in range(
                        -(sensor.beacon_distance + 1), sensor.beacon_distance + 1
                    )
                ]
            )

            # for position in already_analyzed.symmetric_difference(possible_locations):
            for position in possible_locations:
                # invalid x or y position
                if (
                    position[0] < min_
                    or position[0] >= max_
                    or position[1] < min_
                    or position[1] >= max_
                ):
                    continue
                # if position is not inside other scanner solution is found
                if not self.is_inside_scanner_range(pos=position):
                    return position
            # already_analyzed.update(possible_locations)


def load_data(filepath: str) -> Sensors:
    """load list of sensor beacon pairs from file"""
    lines = read_lines_as_list(fp=filepath, split=": ")
    sensors: Sensors = []
    for sensor_str, beacon_str in lines:
        sensor_x, sensor_y = sensor_str[12:].split(", ")
        beacon_x, beacon_y = beacon_str[23:].split(", ")
        sensors.append(
            Sensor(
                sensor_pos=(int(sensor_x), int(sensor_y[2:])),
                beacon_pos=(int(beacon_x), int(beacon_y[2:])),
            )
        )
    return sensors


class Test2022Day15(unittest.TestCase):
    test_sensors: Sensors = load_data("data/15-test.txt")
    test_map: SensorBeaconMap = SensorBeaconMap(sensors=test_sensors)

    def test_can_not_be_distress_beacon(self):
        for pos, beacon in [
            ((0, 9), True),
            ((0, 11), True),
            ((1, 11), True),
            ((2, 10), False),
            ((-2, 9), False),
            ((24, 9), False),
            ((20, 9), True),
            ((14, 11), False),
        ]:
            with self.subTest(msg=f"pos: {pos}"):
                self.assertEqual(self.test_map.can_not_be_distress_beacon(pos), beacon)

    def test_can_not_be_beacon(self):
        for pos, beacon in [
            ((0, 9), True),
            ((0, 11), True),
            ((1, 11), True),
            ((2, 10), True),
            ((-2, 9), False),
            ((24, 9), False),
            ((20, 9), True),
            ((14, 11), False),
        ]:
            with self.subTest(msg=f"pos: {pos}"):
                self.assertEqual(self.test_map.is_inside_scanner_range(pos), beacon)

    def test_can_be_distress_beacon(self):
        for pos, beacon in [
            ((0, 9), False),
            ((0, 11), False),
            ((1, 11), False),
            ((2, 10), False),
            ((-2, 9), True),
            ((24, 9), True),
            ((20, 9), False),
            ((14, 11), True),
        ]:
            with self.subTest(msg=f"pos: {pos}"):
                self.assertEqual(self.test_map.can_be_beacon(pos), beacon)

    def test_count_non_beacon_naive(self):
        # from x = -8 -> 26
        for y, amount in [
            (9, 25),
            (10, 26),
            (11, 28),
        ]:
            with self.subTest(msg=f"y: {y}"):
                self.assertEqual(self.test_map.count_non_beacon_naive(y), amount)

    def test_count_where_distress_isnt(self):
        # from x = -8 -> 26
        for y, amount in [
            (9, 25),
            (10, 26),
            (11, 27),
        ]:
            with self.subTest(msg=f"y: {y}"):
                self.assertEqual(self.test_map.count_where_distress_isnt(y), amount)

    def test_find_distress_signal_position_naive(self):
        self.assertEqual(
            self.test_map.find_distress_signal_location_naive(max_=20), (14, 11)
        )

    def test_find_distress_signal_position_faster(self):
        self.assertEqual(
            self.test_map.find_distress_signal_location_faster(max_=20), (14, 11)
        )


if __name__ == "__main__":
    print(">>> Start Main 15:")
    puzzle_input: Sensors = load_data("data/15.txt")
    puzzle_map: SensorBeaconMap = SensorBeaconMap(sensors=puzzle_input)
    print("Part 1): ", puzzle_map.count_where_distress_isnt(2_000_000))  # 4919281
    # TODO Speedup even even more? takes ~ minute
    loc = puzzle_map.find_distress_signal_location_faster()
    print(loc)
    print("Part 2): ", loc[0] * 4_000_000 + loc[1])  # 12630143363767
    print("End Main 15<<<")
