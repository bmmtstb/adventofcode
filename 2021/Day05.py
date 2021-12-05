import unittest
from parameterized import parameterized
from typing import Dict, List, Tuple, Set

from helper.file import read_lines_as_list

coord = Tuple[int, int]


def parse_input(filepath) -> List[List[coord]]:
    """read the file and parse the inputs"""
    data: List[List[str]] = read_lines_as_list(filepath, split=" -> ")
    line_infos: List[List[coord]] = []
    for line in data:
        line_info: List[coord] = []
        for val in line:
            x, y = val.strip().split(",")
            pos: coord = (int(x), int(y))
            line_info.append(pos)
        line_infos.append(line_info)
    return line_infos




def generate_line_points(start: coord, end: coord, diag: bool) -> List[coord]:
    """generate vertical and horizontal points between start and end - integer only"""
    step1: int = 1 if start[1] <= end[1] else -1
    step0: int = 1 if start[0] <= end[0] else -1
    if start[0] == end[0]:
        return [(start[0], i) for i in range(start[1], end[1] + step1, step1)]
    elif start[1] == end[1]:
        return [(i, start[1]) for i in range(start[0], end[0] + step0, step0)]
    elif diag and abs(start[0] - end[0]) == abs(start[1] - end[1]):
        return [(start[0] + step0 * i, start[1] + step1 * i) for i in range(abs(start[0] - end[0]) + 1)]
    else:
        return []


def count_per_field(points: List[coord]) -> Dict[coord, int]:
    """per coordinate, count how often it appears for the generated points"""
    d: Dict[coord, int] = {}
    for point in points:
        if point in d.keys():
            d[point] += 1
        else:
            d[point] = 1
    return d



def analyze_area(line_data: List[List[coord]], threshold: int, diag: bool = False) -> int:
    """for a given line data, count how many points are over a given threshold"""
    points: List[coord] = []
    for line in line_data:
        points += generate_line_points(line[0], line[1], diag)
    counts = count_per_field(points)
    return sum(1 if pos_val >= threshold else 0 for pos_val in counts.values())



class Test2021Day05(unittest.TestCase):

    @parameterized.expand([
        [(0, 9), (5, 9), [(0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9)]],
        [(0, 8), (8, 0), []],
        [(9, 4), (3, 4), [(9, 4), (8, 4), (7, 4), (6, 4), (5, 4), (4, 4), (3, 4)]],
        [(9, 6), (9, 4), [(9, 6), (9, 5), (9, 4)]]
    ])
    def test_horiz_vert_lines(self, s, e, pts):
        self.assertEqual(generate_line_points(s, e, diag=False), pts)

    def test_test_data_h_v(self):
        self.assertEqual(analyze_area(parse_input("data/05-test.txt"), 2, diag=False), 5)

    @parameterized.expand([
        [(1, 1), (2, 2), [(1, 1), (2, 2)]],
        [(1, 2), (3, 4), [(1, 2), (2, 3), (3, 4)]],
        [(10, 8), (8, 6), [(10, 8), (9, 7), (8, 6)]],
        [(8, 10), (10, 8), [(8, 10), (9, 9), (10, 8)]],
        [(5, 5), (8, 2), [(5, 5), (6, 4), (7, 3), (8, 2)]],
    ])
    def test_diag_lines(self, s, e, pts):
        self.assertEqual(generate_line_points(s, e, diag=True), pts)

    def test_test_data_diag(self):
        self.assertEqual(analyze_area(parse_input("data/05-test.txt"), 2, diag=True), 12)




if __name__ == '__main__':
    print(">>> Start Main 05:")
    puzzle_input = parse_input("data/05.txt")
    print("Part 1): ", analyze_area(puzzle_input, 2))
    print("Part 2): ", analyze_area(puzzle_input, 2, diag=True))
    print("End Main 05<<<")
