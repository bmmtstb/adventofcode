import unittest
from parameterized import parameterized
from typing import Dict, List, Tuple, Set


def load_data(filepath: str) -> List[tuple]:
    """create array of instructions from datafile"""
    data = []
    with open(filepath) as file:
        for line in file.readlines():
            line.replace("\n", "")
            if line.startswith("mem"):
                key, value = line.split("=")
                mem, pointer = key.strip().split("[")
                pointer = int(pointer.split("]")[0])
                value = int(value.strip())
                data.append((mem, pointer, value))
            elif line.startswith("mask"):
                s, mask = line.split("=")
                data.append((s.strip(), str(mask.strip())))
            else:
                raise Exception("Bad parameter in line: {} while reading file {}".format(line, filepath))
    return data


def run_init_program(code: List[tuple]) -> Dict[int, str]:
    """Run the init program by updating mask and memory accordingly"""
    init_mask = "X" * 36  # 36 bit
    # init_mem = "0" * 36  # 36 bit
    mem = {}  # dict of address -> mem

    curr_mask = init_mask
    for cmd in code:
        if cmd[0] == "mask":
            curr_mask = cmd[1]
        elif cmd[0] == "mem":
            byte = '{0:036b}'.format(cmd[2])
            masked = "0b" + "".join(map(lambda m, b: b if m == "X" else m, curr_mask, byte))
            mem[cmd[1]] = masked
        else:
            raise Exception("Command {} not expected".format(cmd[0]))
    return mem


class Test2020Day14(unittest.TestCase):
    @parameterized.expand([
        ["data/14-test.txt", {7: "0b000000000000000000000000000001100101", 8: "0b000000000000000000000000000001000000"}],
    ])
    def test_(self, fname, state):
        self.assertEqual(run_init_program(load_data(fname)), state)


if __name__ == '__main__':
    print(">>> Start Main 14:")
    puzzle_input = load_data("data/14.txt")
    print("Part 1):")
    state = run_init_program(puzzle_input)
    print(sum(int(c, 2) for c in state.values()))
    print("Part 2):")
    print("End Main 14<<<")
