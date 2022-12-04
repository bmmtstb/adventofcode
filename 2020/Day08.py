import unittest
from typing import List, Tuple
from copy import deepcopy

puzzle_input = ...


def read_instructions(filepath: str) -> List[Tuple[str, int]]:
    """Read a list of instructions"""
    instructions = []
    with open(filepath) as file:
        for line in file.readlines():
            instruction, value = line.replace("\n", "").split(" ")
            instructions.append((instruction, int(value)))
    return instructions


def run_instructions_till_loop(instructions: List[Tuple[str, int]], acc: int = 0, pointer: int = 0) -> Tuple[bool, int]:
    """Run instructions until an instruction is run a second time. Returns whether or not completed successfully and
    the current acc stack """
    visited = []
    while 0 <= pointer < len(instructions):
        if pointer in visited:
            return False, acc
        instr, value = instructions[pointer]
        visited.append(pointer)
        if instr == "nop":
            pointer += 1
        elif instr == "acc":
            acc += value
            pointer += 1
        elif instr == "jmp":
            pointer += value
        else:
            raise Exception("Instruction code {} is not expected.".format(instr))
    return True, acc


def repair_instructions(instructions: List[Tuple[str, int]]) -> int:
    """Change one instruction from jmp to nop or nop to jump and try to repair the code"""
    acc = 0
    valid = False
    change_pointer = 0
    while not valid:
        if change_pointer > len(instructions):
            raise Exception("Could not find a suitable solution.")
        new_instr = deepcopy(instructions)
        curr_op, curr_val = new_instr[change_pointer]
        # change current instruction if necessary and run the changed code
        if curr_op == "nop":
            new_instr[change_pointer] = ("jmp", curr_val)
            valid, acc = run_instructions_till_loop(new_instr)
        elif curr_op == "jmp":
            new_instr[change_pointer] = ("nop", curr_val)
            valid, acc = run_instructions_till_loop(new_instr)
        change_pointer += 1
    return acc


class Test2020Day08(unittest.TestCase):
    def test_loop_terminating(self):
        self.assertEqual(run_instructions_till_loop(read_instructions("data/08-test.txt"))[1], 5)

    def test_change_loop(self):
        self.assertEqual(repair_instructions(read_instructions("data/08-test.txt")), 8)


if __name__ == '__main__':
    print(">>> Start Main 08:")
    puzzle_input = read_instructions("data/08.txt")
    print("Part 1):")
    print(run_instructions_till_loop(puzzle_input))
    print("Part 2):")
    print(repair_instructions(puzzle_input))
    print("End Main 08<<<")
