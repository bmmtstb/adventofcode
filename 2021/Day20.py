import unittest
from copy import deepcopy
from typing import Dict, List, Tuple, Set

from helper.file import load_file_and_split
from helper.tuple import tuple_add_tuple

Algorithm = List[int]
Image = List[List[int]]


def load(filepath: str) -> (Algorithm, Image):
    """
    load and convert
    . -> 0
    # -> 1
    """

    def replace(s: str) -> List[int]:
        return [1 if char == "#" else 0 for char in s]

    algo, image = load_file_and_split(filepath, sep="\n\n")[:2]
    algo_clean = replace(algo)
    image_clean = [replace(line) for line in image.split("\n")][:-1]
    return algo_clean, image_clean


def count_lit(i: Image) -> int:
    """given an image count the number of active pixels"""
    return sum(sum(line) for line in i)


def get_neighboring_value(i: Image, pos: Tuple[int, int], filler: int = 0) -> int:
    """
    given an image and a position get a list of the nine neighboring values
    then using its binary representation, cast it to int
    padding: zero-padding on all sides (infinite image)
    """
    positions = [tuple_add_tuple(pos, mod) for mod in [(-1, -1), (0, -1), (1, -1),
                                                       (-1, 0), (0, 0), (1, 0),
                                                       (-1, 1), (0, 1), (1, 1)]]
    values = [i[p[1]][p[0]] if 0 <= p[0] < len(i[0]) and 0 <= p[1] < len(i) else filler for p in positions]
    # concat as string then use base 2 and return value
    return int("".join(str(v) for v in values), 2)


def image_enhancement(algo: Algorithm, img: Image, n: int = 2) -> Image:
    """
    create a new image that is one bigger on every side than the original, then enhance using get_neighbors
    """
    for i in range(n):
        img = [[algo[
                      get_neighboring_value(img, (x, y), filler=(i % 2 if algo[0] == 1 and algo[-1] == 0 else 0))
                  ] for x in range(-1, len(img[0]) + 1)] for y in range(-1, len(img) + 1)]
    return img


class Test2021Day20(unittest.TestCase):
    test_algo, test_image = load("data/20-test.txt")

    def test_active(self):
        for i, lit in [
            (0, 10),
            (1, 24),
            (2, 35),
            (50, 3351),
        ]:
            with self.subTest(msg=f'count_lit - {i}'):
                self.assertEqual(lit, count_lit(image_enhancement(self.test_algo, deepcopy(self.test_image), n=i)))

    def test_get_neighboring_pixels(self):
        for pos, num in [
            ((2, 2), 34),
            ((-1, -1), 1),
            ((0, 0), 18),
            ((4, 4), 48),
            ((2, 0), 8),
            ((0, 2), 152),
        ]:
            with self.subTest(msg=f'get_neighboring_value - {pos}'):
                self.assertEqual(num, get_neighboring_value(deepcopy(self.test_image), pos))


if __name__ == '__main__':
    print(">>> Start Main 20:")
    puzzle_algo, puzzle_image = load("data/20.txt")
    print("Part 1): ", count_lit(image_enhancement(deepcopy(puzzle_algo), deepcopy(puzzle_image), n=2)))
    print("Part 2): ", count_lit(image_enhancement(deepcopy(puzzle_algo), deepcopy(puzzle_image), n=50)))
    print("End Main 20<<<")
