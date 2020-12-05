import unittest
from parameterized import parameterized


def read_file(filepath):
    """reads the file at filepath"""
    data = []
    with open(filepath) as file:
        for line in file.readlines():
            data.append(line.replace("\n", ""))
    return data


def get_row(s: str):
    """get row number (0..127) from string of form "FBFFFFF" 7-digit binary front/back"""
    b = "0b" + "".join("0" if c == "F" else "1" for c in s)
    return int(b, 2)


def get_column(s: str):
    """get column number (0..7) from string of for "RLR" 3-digit binary left/right"""
    b = "0b" + "".join("0" if c == "L" else "1" for c in s)
    return int(b, 2)


def get_seat_id(s: str):
    """given seat binary code, calculate seat id"""
    r = get_row(s[:-3])
    c = get_column(s[-3:])
    return r * 8 + c


class TestDay05(unittest.TestCase):

    @parameterized.expand([
        ["BFFFBBFRRR", 70],
        ["FFFBBBFRRR", 14],
        ["BBFFBBFRLL", 102],
        ["BBBBBBBRRR", 127],
    ])
    def test_row_numbers(self, code, row):
        self.assertEqual(get_row(code[:-3]), row)

    @parameterized.expand([
        ["BFFFBBFRRR", 7],
        ["FFFBBBFRRR", 7],
        ["BBFFBBFRLL", 4],
        ["BBBBBBBLLL", 0],
    ])
    def test_col_numbers(self, code, col):
        self.assertEqual(get_column(code[-3:]), col)

    @parameterized.expand([
        ["BFFFBBFRRR", 567],
        ["FFFBBBFRRR", 119],
        ["BBFFBBFRLL", 820],
        ["BBBBBBBRRR", 1023],
    ])
    def test_seat_id(self, code, sid):
        self.assertEqual(get_seat_id(code), sid)


if __name__ == '__main__':
    print(">>> Start Main 05:")
    puzzle_input = read_file("data/Day05.txt")
    print("Part 1):")
    sids = []
    for seat in puzzle_input:
        sids.append(get_seat_id(seat))
    print(max(sids))
    print("Part 2):")
    for seat in range(min(sids), max(sids)):
        if seat not in sids and seat - 1 in sids and seat + 1 in sids:
            print(seat)
    print("End Main 05<<<")
