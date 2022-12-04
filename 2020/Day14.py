import unittest
from typing import Dict, List


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


def generate_possibilities(codes: List[str]) -> List[str]:
    """replace one X in every code with 0 and 1"""
    new_possibilities = []
    for code in codes:
        if code.count("X") == 0:
            new_possibilities.append(code)
        else:
            idx = code.find("X")
            c0 = code[:idx] + "0" + code[idx + 1:]
            c1 = code[:idx] + "1" + code[idx + 1:]
            new_possibilities += generate_possibilities([c0, c1])
    return new_possibilities




def run_variant2(code: List[tuple]) -> Dict[int, int]:
    """Run the program with floating values"""
    init_mask = "X" * 36  # 36 bit
    init_mem = "0" * 36  # 36 bit
    mem = {}  # memory and address

    curr_mask = init_mask
    for cmd in code:
        if cmd[0] == "mask":
            curr_mask = cmd[1]
        elif cmd[0] == "mem":
            byte = '{0:036b}'.format(cmd[1])
            masked = "".join(map(lambda mask, b: "X" if mask == "X" else b if mask == "0" else "1", curr_mask, byte))
            # check for floating values in masked and add to mem
            for new in generate_possibilities([masked]):
                mem[int("0b"+new, 2)] = cmd[2]
        else:
            raise Exception("Command {} not expected".format(cmd[0]))
    return mem



class Test2020Day14(unittest.TestCase):
    def test_v1(self):
        self.assertEqual(run_init_program(load_data("data/14-test.txt")), {7: "0b000000000000000000000000000001100101", 8: "0b000000000000000000000000000001000000"})

    def test_v2(self):
        d = run_variant2(load_data("data/14-test2.txt"))
        self.assertEqual(sum(c for c in d.values()), 208)


if __name__ == '__main__':
    print(">>> Start Main 14:")
    puzzle_input = load_data("data/14.txt")
    print("Part 1):")
    state = run_init_program(puzzle_input)
    print(sum(int(c, 2) for c in state.values()))
    print("Part 2):")
    variant = run_variant2(puzzle_input)
    print((sum(c for c in variant.values())))
    print("End Main 14<<<")
