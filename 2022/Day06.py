import unittest
from typing import Dict, List, Tuple, Set

from helper.file import read_lines_as_list


# TODO goal was to use binary character representation and logical or


def get_start_of_packet_marker(datastream: str, length: int = 4) -> int:
    """get the start of a packet marker. First occurrence where length characters are non-equal"""
    for i in range(length, len(datastream)):
        stream_slice: set = set(datastream[i - length : i])
        if len(stream_slice) == length:
            return i
    return -1


class Test2022Day06(unittest.TestCase):
    def test_get_start_of_packet_marker(self):
        for string, length, packet_start in [
            ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4, 7),
            ("bvwbjplbgvbhsrlpgdmjqwftvncz", 4, 5),
            ("nppdvjthqldpwncqszvftbrmjlhg", 4, 6),
            ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4, 10),
            ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4, 11),
            ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14, 19),
            ("bvwbjplbgvbhsrlpgdmjqwftvncz", 14, 23),
            ("nppdvjthqldpwncqszvftbrmjlhg", 14, 23),
            ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14, 29),
            ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14, 26),
        ]:
            with self.subTest(msg=f""):
                self.assertEqual(
                    get_start_of_packet_marker(string, length=length), packet_start
                )


if __name__ == "__main__":
    print(">>> Start Main 06:")
    puzzle_input: str = read_lines_as_list("data/06.txt")[0]
    print("Part 1): ", get_start_of_packet_marker(puzzle_input))
    print("Part 2): ", get_start_of_packet_marker(puzzle_input, length=14))
    print("End Main 06<<<")
