import unittest

import numpy as np
from scipy.ndimage import binary_fill_holes
from scipy.signal import convolve


KERNEL = np.array(
    [
        [[0, 0, 0], [0, -1, 0], [0, 0, 0]],
        [[0, -1, 0], [-1, 6, -1], [0, -1, 0]],
        [[0, 0, 0], [0, -1, 0], [0, 0, 0]],
    ]
)


class Positions:
    def __init__(self, coords: np.ndarray):
        self.max_ = np.max(coords, axis=0) + 1
        # self.min_ = np.min(coords, axis=0)
        self.area = np.zeros(self.max_, dtype=int)
        for coord in coords:
            self.area[tuple(coord)] = 1

    def get_total_surface_area(self, fill_holes: bool = False) -> int:
        """use convolution and multiplication to get area count"""
        duplicate_area = self.area.copy()

        if fill_holes:
            duplicate_area = binary_fill_holes(duplicate_area)
        # use convolution to get in place correct values of blocks
        # make sure to multiply it with original to only get count of blocks directly, not neighbors
        return (
            convolve(duplicate_area, KERNEL.copy(), mode="same") * duplicate_area
        ).sum()


class Test2022Day18(unittest.TestCase):
    test_coordinates: np.ndarray = np.loadtxt(
        "data/18-test.txt", delimiter=",", dtype=int
    )
    # test_positions: Positions = Positions(test_coordinates)

    def test_get_surface_area(self):
        for coords, surface_area in [
            (self.test_coordinates.copy(), 64),
            (np.array([[1, 1, 1], [2, 1, 1]]), 10),
            (np.array([[1, 1, 1], [1, 2, 1]]), 10),
            (np.array([[1, 1, 1], [1, 1, 2]]), 10),
            (np.array([[1, 1, 1], [2, 1, 1], [3, 1, 1]]), 14),
            (np.array([[1, 1, 1], [2, 2, 2]]), 12),
            (np.array([[1, 1, 1], [2, 1, 2]]), 12),
        ]:
            with self.subTest(msg=f"coords: {coords}, surface: {surface_area}"):
                self.assertEqual(
                    Positions(coords).get_total_surface_area(), surface_area
                )

    def test_exterior_surface_area(self):
        self.assertEqual(
            Positions(self.test_coordinates.copy()).get_total_surface_area(
                fill_holes=True
            ),
            58,
        )


if __name__ == "__main__":
    print(">>> Start Main 18:")
    puzzle_input: Positions = Positions(
        np.loadtxt("data/18.txt", delimiter=",", dtype=int)
    )
    print("Part 1): ", puzzle_input.get_total_surface_area())
    print("Part 2): ", puzzle_input.get_total_surface_area(fill_holes=True))
    print("End Main 18<<<")
