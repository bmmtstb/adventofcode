import unittest
from typing import Dict, List, Tuple, Set

from helper.file import load_file_and_split

# probe from Day17 sends out beacons and scanners
# everything is motionless
# using 12 points figure out rotation [multiple of 90 deg]

Coord = Tuple[int, ...]
Coords = List[Coord]
Scanners = List[Coords]


class NoMatchingBeacons(Exception):
    pass


def load_from_file(filepath: str) -> Scanners:
    """load configuration from filepath"""
    scanners = load_file_and_split(filepath=filepath, separator="\n\n", instance_type=str)
    return [[
        tuple(int(val) for val in loc.strip().split(",")) for loc in scanner.split("\n")[1:]
    ] for scanner in scanners]


def match_all_scanners(scanners: Scanners, limit: int = 12) -> (Coords, Coords):
    """
    given multiple scanners, try to combine two until all are matched
    returns all coords and all scanner positions given coord-frame of scanner 1
    """
    all_beacons: Coords = scanners[0]
    all_scanners: Coords = [(0, 0, 0)]
    remaining_scanners = scanners[1:]
    i = 0
    while len(remaining_scanners) > 0:
        # try to find the next scanner with enough overlapping beacons
        try:
            all_beacons, new_scanner = match_two_scanners(coords1=all_beacons, coords2=remaining_scanners[i], limit=limit)
            all_scanners.append(new_scanner)
            remaining_scanners.pop(i)
        except NoMatchingBeacons:
            continue
        finally:
            i += 1
            i %= len(remaining_scanners)
    return all_beacons, all_scanners


def match_two_scanners(coords1: Coords, coords2: Coords, limit: int = 12) -> (Coords, Coord):
    """
    given two list of coordinates combine them into one
    returns all coords in one list (if possible) and the second scanner's position both given the first coordinate frame
    """
    if min(len(coords1), len(coords2)) < limit:
        raise NoMatchingBeacons
    return ..., ...


# class Test2021Day19(unittest.TestCase):
#
    # def test_tiny_example(self):
    #     base_case_scanners: Scanners = [
    #         [(0, 2), (4, 1), (3, 3)],
    #         [(-1, -1), (-5, 0), (-2, 1)],
    #     ]
    #     positions, pos_scan2 = match_two_scanners(base_case_scanners[0], base_case_scanners[1], limit=3)
    #     self.assertEqual(positions, base_case_scanners[0])
    #     self.assertEqual(pos_scan2, (5, 2, 2))
    #     all_positions, all_scanners = match_all_scanners(base_case_scanners, limit=3)
    #     self.assertListEqual(all_positions, positions)
    #     self.assertListEqual(all_scanners, [(0, 0, 0), (5, 2, 2)])
    #
    # def test_example(self):
    #     first_scanner_positions = [(0, 0, 0), (68, -1246, -43), (1105, -1205, 1229), (-92, -2380, -20), (-20, -1133, 1061)]
    #
    #     beacon_positions = [(-892, 524, 684), (-876, 649, 763), (-838, 591, 734), (-789, 900, -551), (-739, -1745, 668), (-706, -3180, -659), (-697, -3072, -689), (-689, 845, -530), (-687, -1600, 576), (-661, -816, -575), (-654, -3158, -753), (-635, -1737, 486), (-631, -672, 1502), (-624, -1620, 1868), (-620, -3212, 371), (-618, -824, -621), (-612, -1695, 1788), (-601, -1648, -643), (-584, 868, -557), (-537, -823, -458), (-532, -1715, 1894), (-518, -1681, -600), (-499, -1607, -770), (-485, -357, 347), (-470, -3283, 303), (-456, -621, 1527), (-447, -329, 318), (-430, -3130, 366), (-413, -627, 1469), (-345, -311, 381), (-36, -1284, 1171), (-27, -1108, -65), (7, -33, -71), (12, -2351, -103), (26, -1119, 1091), (346, -2985, 342), (366, -3059, 397), (377, -2827, 367), (390, -675, -793), (396, -1931, -563), (404, -588, -901), (408, -1815, 803), (423, -701, 434), (432, -2009, 850), (443, 580, 662), (455, 729, 728), (456, -540, 1869), (459, -707, 401), (465, -695, 1988), (474, 580, 667), (496, -1584, 1900), (497, -1838, -617), (527, -524, 1933), (528, -643, 409), (534, -1912, 768), (544, -627, -890), (553, 345, -567), (564, 392, -477), (568, -2007, -577), (605, -1665, 1952), (612, -1593, 1893), (630, 319, -379), (686, -3108, -505), (776, -3184, -501), (846, -3110, -434), (1135, -1161, 1235), (1243, -1093, 1063), (1660, -552, 429), (1693, -557, 386), (1735, -437, 1738), (1749, -1800, 1813), (1772, -405, 1572), (1776, -675, 371), (1779, -442, 1789), (1780, -1548, 337), (1786, -1538, 337), (1847, -1591, 415), (1889, -1729, 1762), (1994, -1805, 1792)]
    #     scanners = load_from_file("data/19-p1.txt")
    #     positions, scanners = match_all_scanners(scanners=scanners, limit=12)
    #     self.assertEqual(79, len(positions))
    #     self.assertListEqual(positions, beacon_positions)
    #     self.assertListEqual(first_scanner_positions, scanners[0:5])
#
#
#
# if __name__ == '__main__':
#     print(">>> Start Main 19:")
#     puzzle_input = []
#     print("Part 1): ")
#     print("Part 2): ")
#     print("End Main 19<<<")
