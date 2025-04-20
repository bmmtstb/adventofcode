import math
import re
import unittest
from copy import copy

from helper.file import load_file_and_split

Registers = dict[str, int]
Program = list[int]


def load_data(fp: str) -> (Registers, Program):
    d = load_file_and_split(fp, sep="\n\n")
    if len(d) != 2:
        raise ValueError(f"Data should contain two parts, but got {len(d)}")
    registers, program = d
    registers = {k: int(v) for k, v in re.findall(r"\s(\w): (\d+)\n*", registers)}
    program = list(map(int, program.split(": ")[-1].split(",")))
    return registers, program


def get_combo_operand(co: int, r) -> int:
    """Get the combo operand."""
    if co <= 3:
        return co
    if co == 4:
        return r["A"]
    if co == 5:
        return r["B"]
    if co == 6:
        return r["C"]
    raise NotImplementedError


def run_program(registers: Registers, program: Program) -> (Registers, list[int]):
    """Run the program with the given registers."""
    instruction_pointer: int = 0
    output: list[int] = []
    while instruction_pointer < len(program):

        registers, new_ip, new_out = execute_opcode(
            opcode=program[instruction_pointer],
            operand=program[instruction_pointer + 1],
            registers=registers,
        )

        # update output
        output += new_out
        # Update the instruction pointer, 2 as long as there is no jump instruction
        if new_ip is not None:
            instruction_pointer = new_ip
        else:
            instruction_pointer += 2

    return registers, output


def execute_opcode(opcode: int, operand: int, registers: Registers) -> (Registers, int | None, list[int]):
    """Given an opcode and the current state of registers, execute the program.

    Returns the updated registers, the instruction pointer after a jump command and possible output values.
    """
    new_instruction_pointer: int | None = None
    output: list[int] = []

    if opcode == 0:  # adv
        # division stored in A
        registers["A"] >>= get_combo_operand(operand, registers)
    elif opcode == 1:  # bxl
        # bitwise XOR
        registers["B"] ^= operand
    elif opcode == 2:  # bst
        # combo mod 8
        registers["B"] = get_combo_operand(operand, registers) % 8
    elif opcode == 3:  # jnz
        # jump if A is not zero
        if registers["A"] != 0:
            new_instruction_pointer = operand
    elif opcode == 4:  # bxc
        # bitwise XOR of register B
        registers["B"] ^= registers["C"]
    elif opcode == 5:  # out
        # combo modulo 8 and output this value
        output.append(get_combo_operand(operand, registers) % 8)
    elif opcode == 6:  # bdv
        # division stored in B
        registers["B"] = registers["A"] >> get_combo_operand(operand, registers)
    elif opcode == 7:  # cdv
        # division stored in C
        registers["C"] = registers["A"] >> get_combo_operand(operand, registers)
    else:
        raise NotImplementedError(f"Opcode {opcode} not implemented")

    return registers, new_instruction_pointer, output


def part1(registers: Registers, program: Program) -> str:
    """Part1: Concat the output values of the program as a string."""
    return run_program(registers, program)


def part2(program: Program) -> int:
    """Part2: Modify register A such that the output values of the program are the program itself.

    Could not find a solution using my functions. Therefore, I used:
    https://github.com/mgtezak/Advent_of_Code/blob/master/2024/17/p2.py
    """
    B: int = 0
    C: int = 0
    n = len(program)

    def run_custom_program(A):

        register = dict(A=A, B=B, C=C)
        i = 0
        out = []
        while i < n:
            opcode, operand = program[i : i + 2]
            match opcode:
                case 0:
                    register["A"] >>= get_combo_operand(operand, register)
                case 1:
                    register["B"] ^= operand
                case 2:
                    register["B"] = get_combo_operand(operand, register) % 8
                case 3:
                    if register["A"]:
                        i = operand - 2
                case 4:
                    register["B"] ^= register["C"]
                case 5:
                    out.append(get_combo_operand(operand, register) % 8)
                case 6:
                    register["B"] = register["A"] >> get_combo_operand(operand, register)
                case 7:
                    register["C"] = register["A"] >> get_combo_operand(operand, register)
            i += 2

        return out

    A = 0
    for i in reversed(range(n)):
        A <<= 3
        while run_custom_program(A) != program[i:]:
            A += 1

    return A


class Test2024Day17(unittest.TestCase):

    fp = "./data/17-test.txt"
    test_data = load_data(fp)
    test_registers, test_program = test_data

    def test_execute_opcode(self):
        for registers, oc, op, out in [
            ({"A": -1, "B": -1, "C": 9}, 2, 6, ({"A": -1, "B": 1, "C": 9}, None, [])),
            ({"A": -1, "B": 29, "C": -1}, 1, 7, ({"A": -1, "B": 26, "C": -1}, None, [])),
            ({"A": -1, "B": 2024, "C": 43690}, 4, 0, ({"A": -1, "B": 44354, "C": 43690}, None, [])),
        ]:
            with self.subTest(msg="registers: {}, oc: {}, op: {}, out: {}".format(registers, oc, op, out)):
                r = execute_opcode(opcode=oc, operand=op, registers=registers)
                self.assertEqual(r, out)

    def test_run_program(self):
        for registers, program, out in [
            ({"A": 10, "B": -1, "C": -1}, [5, 0, 5, 1, 5, 4], ({"A": 10, "B": -1, "C": -1}, [0, 1, 2])),
            (
                {"A": 2024, "B": -1, "C": -1},
                [0, 1, 5, 4, 3, 0],
                ({"A": 0, "B": -1, "C": -1}, [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]),
            ),
            (self.test_registers, self.test_program, ({"A": 0, "B": 0, "C": 0}, [4, 6, 3, 5, 6, 3, 5, 2, 1, 0])),
        ]:
            with self.subTest(msg="registers: {}, program: {}, out: {}".format(registers, program, out)):
                r = run_program(registers=registers, program=program)
                self.assertEqual(r, out)

    # def test_part2(self):
    #     self.assertEqual(part2(self.test_program), 117440)


if __name__ == "__main__":
    print(">>> Start Main 17:")
    puzzle_data = load_data("./data/17.txt")
    out1 = part1(*puzzle_data)[1]
    print("Part 1): ", ",".join(str(n) for n in out1) if len(out1) else "")
    print("Part 2): ", part2(puzzle_data[1]))  # 37221270076916
    print("End Main 17<<<")
