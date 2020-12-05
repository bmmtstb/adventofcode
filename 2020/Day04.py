import unittest
from parameterized import parameterized
import string


def load_passports_from_file(filepath):
    """read all passports from a given file"""
    pass_list = []
    with open(filepath) as file:
        current = {}
        for line in file.readlines():
            # end of current passport
            if line == "\n":
                pass_list.append(current)
                current = {}
            # read passport
            else:
                fields = line.removesuffix("\n").split(" ")
                for field in fields:
                    field_id, field_value = field.split(":")
                    if field_id in current.keys():
                        raise Exception("Same Key twice: " + str(field_id))
                    current[str(field_id)] = field_value
        if current.keys():
            pass_list.append(current)
    return pass_list


# Expected Fields:
# byr (Birth Year)
# iyr (Issue Year)
# eyr (Expiration Year)
# hgt (Height)
# hcl (Hair Color)
# ecl (Eye Color)
# pid (Passport ID)
# cid (Country ID) [optional]
regular_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}
northpole_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}


def passport_has_all_fields(passport: dict):
    """Check if a passport has all valid keys"""
    keys = set(passport.keys())
    return regular_fields.issubset(keys) or northpole_fields.issubset(keys)


def is_number_in_range(s, lower, upper):
    """checks if a string is numeric and within a given range"""
    return not s.isnumeric() or int(s) < lower or int(s) > upper


def passport_fields_valid(passport: dict):
    """Checks if the values of a passport are correct"""
    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    if is_number_in_range(passport["byr"], 1920, 2002):
        return False
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    if is_number_in_range(passport["iyr"], 2010, 2020):
        return False
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    if is_number_in_range(passport["eyr"], 2020, 2030):
        return False
    # hgt (Height) - a number followed by either cm or in:
    #     If cm, the number must be at least 150 and at most 193.
    #     If in, the number must be at least 59 and at most 76.
    if passport["hgt"][-2:] == "cm":
        if is_number_in_range(passport["hgt"][:-2], 150, 193):
            return False
    elif passport["hgt"][-2:] == "in":
        if is_number_in_range(passport["hgt"][:-2], 59, 76):
            return False
    else:
        return False
    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    if passport["hcl"][0] != "#" or len(passport["hcl"]) != 7 or \
            any(not (c.isnumeric() or c in ["a", "b", "c", "d", "e", "f"]) for c in passport["hcl"][1:]):
        return False
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth
    if not passport["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return False
    # pid (Passport ID) - a nine-digit number, including leading zeroes
    if not passport["pid"].isnumeric() or len(passport["pid"]) != 9 or not all(0 <= int(c) <= 9 for c in passport["pid"]):
        return False
    # cid (Country ID) - ignored, missing or not
    return True


def count_valid_passports(passports: list):
    """get a list of passports and count validity"""
    valid_keys = 0
    valid_values = 0
    for passport in passports:
        if passport_has_all_fields(passport):
            valid_keys += 1
            if passport_fields_valid(passport):
                valid_values += 1
    return valid_keys, valid_values


class TestDay04(unittest.TestCase):
    @parameterized.expand([
        ["data/04-Test.txt", 2],
        ["data/04.txt", 208],
    ])
    def test_count_valid(self, fname, valid):
        self.assertEqual(count_valid_passports(load_passports_from_file(fname))[0], valid)

    @parameterized.expand([
        ["data/04-valid.txt", 4],
        ["data/04-invalid.txt", 0],
        ["data/04.txt", 167],
    ])
    def test_count_valid_advanced(self, fname, valid):
        self.assertEqual(count_valid_passports(load_passports_from_file(fname))[1], valid)


if __name__ == '__main__':
    print(">>> Start Main 04:")
    puzzle_input = load_passports_from_file("data/04.txt")
    valid = count_valid_passports(puzzle_input)
    print("Part 1):")
    print(valid[0])
    print("Part 2):")
    print(valid[1])
    print("End Main 04<<<")
