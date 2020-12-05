import unittest
from parameterized import parameterized


def load_data(filename="data/02.txt"):
    """load the data into a usable format"""
    data = []
    cast_int = int
    with open(filename) as file:
        for l in file.readlines():
            words = l.split(" ")
            data.append({
                "policy": tuple([
                    tuple(map(cast_int, words[0].split("-"))),
                    words[1].replace(":", "")
                ]),
                "pw": words[2].replace("\n", ""),
            })
    return data


def get_valid_passwords_counting(dataset):
    """check give data (policy and passwords) for valid passwords"""
    valid = 0
    for data in dataset:
        letter: str = data["policy"][1]
        lmin, lmax = data["policy"][0]
        found = []
        for idx, char in enumerate(data["pw"]):
            if char == letter:
                found.append(idx)
        if lmin <= len(found) <= lmax:
            valid += 1
    return valid


def get_valid_passwords_indexed(dataset):
    """check given data (policy and pw) for valid passwords"""
    valid = 0
    for data in dataset:
        letter: str = data["policy"][1]
        lmin, lmax = data["policy"][0]
        if bool(data["pw"][lmin - 1] == letter) ^ bool(data["pw"][lmax - 1] == letter):
            valid += 1
    return valid


class TestDay02(unittest.TestCase):
    @parameterized.expand([
        ["data/02-Test.txt", 2]
    ])
    def test(self, fname, valid):
        self.assertEqual(get_valid_passwords_counting(load_data(fname)), valid)

    @parameterized.expand([
        ["data/02-Test.txt", 1]
    ])
    def test(self, fname, valid):
        self.assertEqual(get_valid_passwords_indexed(load_data(fname)), valid)


if __name__ == '__main__':
    print(">>> Start Main 2:")
    puzzle_input = load_data()
    print("Part 1):")
    print(get_valid_passwords_counting(puzzle_input))
    print("Part 2):")
    print(get_valid_passwords_indexed(puzzle_input))
    print("End Main 2<<<")
