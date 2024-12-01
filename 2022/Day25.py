import unittest
import math
from typing import Dict, List, Tuple, Set

from helper.file import read_lines_as_list

SYMBOL_CONVERSION: Dict[str, int] = {
    "0": 0,
    "1": 1,
    "2": 2,
    "-": -1,
    "=": -2,
}

DEC_CONVERSION: Dict[int, str] = {
    0: "0",
    1: "1",
    2: "2",
    -1: "-",
    -2: "=",
}


def convert_decimal_to_snafu(dec: int) -> str:
    """convert given decimal number to SNAFU number"""
    # make list one longer than necessary, because there may be overflow
    str_length = math.ceil(math.log(dec, 5)) + 1
    # start at one
    exponent = 1
    quinary_factors: List[int] = [0] * str_length
    rest = dec
    # modify pos of Quinary number
    while exponent < str_length + 1:
        # on the first place use mod 5, not mod 1 -> start exponent at 1 not zero
        current_multiplier = 5 ** (exponent - 1)
        next_multiplier = 5**exponent
        current_quinary_factor = (rest % next_multiplier) // current_multiplier
        # if we get a 3 or 4, convert them to -2 and -1 respectively
        if current_quinary_factor > 2:
            current_quinary_factor = current_quinary_factor - 5
        # save current factor - due to start
        quinary_factors[str_length - exponent] = current_quinary_factor
        # update rest
        rest -= current_multiplier * current_quinary_factor
        # move on to the next power of 5
        exponent += 1
    assert rest == 0
    # convert to symbols
    snafu_str = "".join(DEC_CONVERSION[factor] for factor in quinary_factors)
    # strip leading zeros
    return snafu_str.lstrip("0")


def convert_snafu_to_decimal(snafu: str) -> int:
    """convert SNAFU number to decimal"""
    result: int = 0
    # Quinary string, go back to front and use powers of 5 of the position
    for pos, char in enumerate(snafu[::-1]):
        result += SYMBOL_CONVERSION[char] * (5**pos)
    return result


def calculate_total_fuel_amount(requirements: List[str]) -> str:
    """sum of the fuel requirements as snafu number"""
    return convert_decimal_to_snafu(
        sum(convert_snafu_to_decimal(snafu) for snafu in requirements)
    )


class Test2022Day25(unittest.TestCase):
    all_pairs: List[Tuple[int, str]] = [
        (1, "1"),
        (2, "2"),
        (3, "1="),
        (4, "1-"),
        (5, "10"),
        (6, "11"),
        (7, "12"),
        (8, "2="),
        (9, "2-"),
        (10, "20"),
        (11, "21"),
        (15, "1=0"),
        (20, "1-0"),
        (31, "111"),
        (32, "112"),
        (37, "122"),
        (107, "1-12"),
        (198, "2=0="),
        (201, "2=01"),
        (353, "1=-1="),
        (906, "12111"),
        (1257, "20012"),
        (1747, "1=-0-2"),
        (2022, "1=11-2"),
        (12_345, "1-0---0"),
        (314_159_265, "1121-1110-1=0"),
    ]

    test_input: List[str] = [
        "1=-0-2",
        "12111",
        "2=0=",
        "21",
        "2=01",
        "111",
        "20012",
        "112",
        "1=-1=",
        "1-12",
        "12",
        "1=",
        "122",
    ]

    def test_dec_to_snafu(self):
        for dec, snafu in self.all_pairs:
            with self.subTest(msg=f"dec: {dec}  ->  {snafu}"):
                self.assertEqual(convert_decimal_to_snafu(dec), snafu)

    def test_snafu_to_dec(self):
        for dec, snafu in self.all_pairs:
            with self.subTest(msg=f"snafu:  {snafu}  ->  {dec}"):
                self.assertEqual(convert_snafu_to_decimal(snafu), dec)

    def test_calculate_fuel_amount(self):
        self.assertEqual(calculate_total_fuel_amount(self.test_input), "2=-1=0")


if __name__ == "__main__":
    print(">>> Start Main 25:")
    puzzle_input = read_lines_as_list("data/25.txt", split="every")
    print("Part 1): ", calculate_total_fuel_amount(puzzle_input.copy()))
    print("Part 2): ", "Merry X-Mas")
    print("End Main 25<<<")
