import unittest
from typing import Dict, List, Tuple, Set
from math import prod
from sys import maxsize

hex_bin_converters = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def hexa_to_bin(s: str) -> str:
    """convert hexadecimal to binary data"""
    return "".join(hex_bin_converters[char] for char in s)


def bin_to_int(s: str) -> int:
    """convert 3 digit bin to int"""
    return int(s, base=2)


def decode_packet(bin_s: str) -> (int, int, int):
    """
    decode current packet,
    :returns current value [Task2], current pointer index, current version sum [Task1]
    """

    def sub_call(type_id: int, loc_p, loc_val_sum, loc_vers_sum) -> (int, int, int):
        """same output as before"""
        sub_val, sub_p, sub_vs = decode_packet(bin_s[loc_p:])
        loc_p += sub_p  # move pointer to beginning of next sub-package

        # update value for part 2
        if type_id == 0:  # sum,
            loc_val_sum += sub_val
        elif type_id == 1:  # prod,
            loc_val_sum *= sub_val
        elif type_id == 2:  # min,
            loc_val_sum = min(loc_val_sum, sub_val)
        elif type_id == 3:  # max,
            loc_val_sum = max(loc_val_sum, sub_val)
        elif type_id == 5:  # >,
            if loc_val_sum is None:
                loc_val_sum = sub_val
            else:
                loc_val_sum = int(loc_val_sum > sub_val)
        elif type_id == 6:  # <,
            if loc_val_sum is None:
                loc_val_sum = sub_val
            else:
                loc_val_sum = int(loc_val_sum < sub_val)
        elif type_id == 7:  # ==,
            if loc_val_sum is None:
                loc_val_sum = sub_val
            else:
                loc_val_sum = int(loc_val_sum == sub_val)
        else:
            raise Exception(f"invalid type ID {type_id}")

        loc_vers_sum += sub_vs  # update version for part 1
        return loc_p, loc_val_sum, loc_vers_sum

    # get header-params
    version: int = bin_to_int(bin_s[:3])
    type_id: int = bin_to_int(bin_s[3:6])

    # case no nested subpackages
    if type_id == 4:
        # literal value, encode single bin number
        p = 6  # set curr pointer
        loop_exit = False
        bin_val = ""
        while not loop_exit:  # find all sub-values until one starts with a "0"
            if bin_s[p] == "0":
                loop_exit = True
            bin_val += bin_s[p+1:p+5]
            p += 5  # move pointer
        return bin_to_int(bin_val), p, version
    else:  # operator contains one or more packets
        p = 6  # pointer

        # ########
        # initialize sub-loop
        # ########

        # set total package value dependant of current package type id
        # prod  - don't multiply with zero
        # >,<,= - set to first value -> None
        # min   - set start to max int
        # sum   - set start to 0
        # max   - set start to 0
        val_sum = 1 if type_id == 1 else None if type_id in [5, 6, 7] else maxsize if type_id == 2 else 0
        # set version sum to own version, sub-packages will be added later
        version_sum = version  # total version sum value

        # get the "length type ID"
        len_type_id = bin_s[p]
        p += 1

        if len_type_id == "0":
            # next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet
            sub_packet_len = bin_to_int(bin_s[p:p+15])
            p += 15
            fin = p + sub_packet_len
            while "1" in bin_s[p:fin]:
                p, val_sum, version_sum = sub_call(type_id, p, val_sum, version_sum)
            return val_sum, fin, version_sum
        else:
            # the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet
            nof_sub_packets = bin_to_int(bin_s[p:p+11])
            p += 11
            for _ in range(nof_sub_packets):
                p, val_sum, version_sum = sub_call(type_id, p, val_sum, version_sum)
            return val_sum, p, version_sum


def load_from_file(filepath) -> str:
    """get string from file"""
    with open(filepath) as file:
        lines = file.readlines()
        if len(lines) != 1:
            raise Exception("encountered multiple lines")
        else:
            return str(lines[0]).replace("\n", "")


class Test2021Day16(unittest.TestCase):
    def test_hexa_bin_conversion(self):
        for s, binary in [
            ("D2FE28", "110100101111111000101000"),
        ]:
            with self.subTest(msg=f'str: {s}, sum: {binary}'):
                self.assertEqual(hexa_to_bin(s), binary)


    def test_version_sum(self):
        for s, vers_sum in [
            ("D2FE28", 6),  # simple literal value
            ("38006F45291200", 9),  # type id 0 with two packages [10, 20]
            ("EE00D40C823060", 14),  # type id 1 with three packages [1,2,3]
            ("8A004A801A8002F478", 16),
            ("620080001611562C8802118E34", 12),
            ("C0015000016115A2E0802F182340", 23),
            ("A0016C880162017C3686B18A3D4780", 31),
        ]:
            with self.subTest(msg=f'str: {s}'):
                bin_input = hexa_to_bin(s)
                ls, _, vs = decode_packet(bin_input)
                self.assertEqual(vs, vers_sum)

    def test_value_sum(self):
        for s, lit_sum in [
            ("D2FE28", 2021),  # simple literal value
            ("C200B40A82", 3),
            ("04005AC33890", 54),
            ("880086C3E88112", 7),
            ("CE00C43D881120", 9),
            ("D8005AC2A8F0", 1),
            ("F600BC2D8F", 0),
            ("9C005AC2F8F0", 0),
            ("9C0141080250320F1802104A08", 1),
        ]:
            with self.subTest(msg=f'str: {s}'):
                bin_input = hexa_to_bin(s)
                ls, _, vs = decode_packet(bin_input)
                if lit_sum is not None:
                    self.assertEqual(ls, lit_sum)


    def test_bin_to_int_conversion(self):
        for s, i in [
            ("000", 0), ("001", 1), ("010", 2), ("011", 3), ("100", 4), ("101", 5), ("110", 6), ("111", 7),
            ("0000", 0), ("1111", 15), ("11111", 31)
        ]:
            with self.subTest(msg=f'str: {s}, int: {i}'):
                self.assertEqual(bin_to_int(s), i)



if __name__ == '__main__':
    print(">>> Start Main 16:")
    puzzle_input = load_from_file("data/16.txt")
    bin_input = hexa_to_bin(puzzle_input)
    decoded = decode_packet(bin_input)
    print("Part 1): ", decoded[2])
    print("Part 2): ", decoded[0])
    print("End Main 16<<<")
