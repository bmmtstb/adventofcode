import unittest
from parameterized import parameterized

puzzle_input = [3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 1002, 114, 19, 224, 1001, 224, -646, 224, 4, 224, 102,
                8, 223, 223, 1001, 224, 7, 224, 1, 223, 224, 223, 1101, 40, 62, 225, 1101, 60, 38, 225, 1101, 30, 29,
                225, 2, 195, 148, 224, 1001, 224, -40, 224, 4, 224, 1002, 223, 8, 223, 101, 2, 224, 224, 1, 224, 223,
                223, 1001, 143, 40, 224, 101, -125, 224, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 3, 224, 1, 224, 223,
                223, 101, 29, 139, 224, 1001, 224, -99, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 2, 224, 1, 224, 223,
                223, 1101, 14, 34, 225, 102, 57, 39, 224, 101, -3420, 224, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 7,
                224, 1, 223, 224, 223, 1101, 70, 40, 225, 1102, 85, 69, 225, 1102, 94, 5, 225, 1, 36, 43, 224, 101, -92,
                224, 224, 4, 224, 1002, 223, 8, 223, 101, 1, 224, 224, 1, 224, 223, 223, 1102, 94, 24, 224, 1001, 224,
                -2256, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 1, 224, 1, 223, 224, 223, 1102, 8, 13, 225, 1101, 36,
                65, 224, 1001, 224, -101, 224, 4, 224, 102, 8, 223, 223, 101, 3, 224, 224, 1, 223, 224, 223, 4, 223, 99,
                0, 0, 0, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1105, 0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005,
                227, 99999, 1005, 0, 256, 1105, 1, 99999, 1106, 227, 99999, 1106, 0, 265, 1105, 1, 99999, 1006, 0,
                99999, 1006, 227, 274, 1105, 1, 99999, 1105, 1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101, 294, 0, 0,
                105, 1, 0, 1105, 1, 99999, 1106, 0, 300, 1105, 1, 99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0,
                1105, 1, 99999, 8, 677, 226, 224, 1002, 223, 2, 223, 1006, 224, 329, 1001, 223, 1, 223, 1108, 226, 226,
                224, 1002, 223, 2, 223, 1005, 224, 344, 101, 1, 223, 223, 1108, 226, 677, 224, 1002, 223, 2, 223, 1006,
                224, 359, 101, 1, 223, 223, 107, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 374, 101, 1, 223, 223,
                1107, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 389, 101, 1, 223, 223, 107, 677, 677, 224, 102, 2,
                223, 223, 1006, 224, 404, 101, 1, 223, 223, 1008, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 419, 101,
                1, 223, 223, 108, 677, 226, 224, 1002, 223, 2, 223, 1006, 224, 434, 101, 1, 223, 223, 1108, 677, 226,
                224, 102, 2, 223, 223, 1005, 224, 449, 101, 1, 223, 223, 1008, 677, 226, 224, 102, 2, 223, 223, 1006,
                224, 464, 1001, 223, 1, 223, 108, 677, 677, 224, 102, 2, 223, 223, 1005, 224, 479, 101, 1, 223, 223, 7,
                677, 677, 224, 102, 2, 223, 223, 1005, 224, 494, 1001, 223, 1, 223, 8, 226, 677, 224, 102, 2, 223, 223,
                1006, 224, 509, 101, 1, 223, 223, 107, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 524, 1001, 223, 1,
                223, 7, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 539, 1001, 223, 1, 223, 1007, 226, 677, 224, 1002,
                223, 2, 223, 1005, 224, 554, 1001, 223, 1, 223, 8, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 569, 101,
                1, 223, 223, 7, 226, 677, 224, 102, 2, 223, 223, 1006, 224, 584, 1001, 223, 1, 223, 1008, 677, 677, 224,
                102, 2, 223, 223, 1005, 224, 599, 101, 1, 223, 223, 1007, 677, 677, 224, 1002, 223, 2, 223, 1006, 224,
                614, 101, 1, 223, 223, 1107, 677, 226, 224, 1002, 223, 2, 223, 1006, 224, 629, 101, 1, 223, 223, 1107,
                226, 677, 224, 1002, 223, 2, 223, 1006, 224, 644, 101, 1, 223, 223, 1007, 226, 226, 224, 102, 2, 223,
                223, 1005, 224, 659, 1001, 223, 1, 223, 108, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 674, 101, 1,
                223, 223, 4, 223, 99, 226]


# parameter modes:
# 0: position mode - current mode, parameter is position of value
# 1: immediate mode - parameter is value

# opcode: two digit number - rightmost two digits of the first value in an instruction

def read_opcode(instruction) -> list:
    """
    Split an opcode into the four respective parts
    """
    five_digit = f"{instruction:05}"
    de = int(five_digit[-2:])
    return list(map(int, five_digit[:-2])) + [de]


def run_intcode_program(intcode: list, program_input: list, show_output: bool = False, pointer_start: int = 0) -> (list, int, list):
    """
    Calculate final intcode sequence given value
    :return: all the outputs as a list, current instruction pointer or None, current intcode or None
    """
    output = []
    instruction_pointer = pointer_start
    while intcode[instruction_pointer] != 99 and instruction_pointer < len(intcode):
        a, b, c, op = read_opcode(intcode[instruction_pointer])
        if op == 1:  # add
            first = intcode[intcode[instruction_pointer + 1]] if c == 0 else intcode[instruction_pointer + 1]
            second = intcode[intcode[instruction_pointer + 2]] if b == 0 else intcode[instruction_pointer + 2]
            intcode[intcode[instruction_pointer + 3]] = first + second
            instruction_pointer += 4
        elif op == 2:  # multiply
            first = intcode[intcode[instruction_pointer + 1]] if c == 0 else intcode[instruction_pointer + 1]
            second = intcode[intcode[instruction_pointer + 2]] if b == 0 else intcode[instruction_pointer + 2]
            intcode[intcode[instruction_pointer + 3]] = first * second
            instruction_pointer += 4
        elif op == 3:  # save
            if len(program_input) == 0:
                return output, instruction_pointer, intcode.copy()
            intcode[intcode[instruction_pointer + 1]] = program_input.pop(0)
            # intcode[intcode[instruction_pointer + 1]] = int(input("Please enter a number: "))
            instruction_pointer += 2
        elif op == 4:  # output
            out = intcode[intcode[instruction_pointer + 1]] if c == 0 else intcode[instruction_pointer + 1]
            if show_output:
                print("Output is: {}".format(out))
            output.append(out)
            instruction_pointer += 2
        elif op == 5:  # jump-if-true
            first = intcode[intcode[instruction_pointer + 1]] if c == 0 else intcode[instruction_pointer + 1]
            second = intcode[intcode[instruction_pointer + 2]] if b == 0 else intcode[instruction_pointer + 2]
            if first != 0:
                instruction_pointer = second
            else:
                instruction_pointer += 3
        elif op == 6:  # jump-if-false
            first = intcode[intcode[instruction_pointer + 1]] if c == 0 else intcode[instruction_pointer + 1]
            second = intcode[intcode[instruction_pointer + 2]] if b == 0 else intcode[instruction_pointer + 2]
            if first == 0:
                instruction_pointer = second
            else:
                instruction_pointer += 3
        elif op == 7:  # less than
            first = intcode[intcode[instruction_pointer + 1]] if c == 0 else intcode[instruction_pointer + 1]
            second = intcode[intcode[instruction_pointer + 2]] if b == 0 else intcode[instruction_pointer + 2]
            intcode[intcode[instruction_pointer + 3]] = 1 if first < second else 0
            instruction_pointer += 4

        elif op == 8:  # equals
            first = intcode[intcode[instruction_pointer + 1]] if c == 0 else intcode[instruction_pointer + 1]
            second = intcode[intcode[instruction_pointer + 2]] if b == 0 else intcode[instruction_pointer + 2]
            intcode[intcode[instruction_pointer + 3]] = 1 if first == second else 0
            instruction_pointer += 4
        else:
            raise ValueError("Something went wrong, opcode {} is not expected.".format(op))
    return output, None, None


class TestSecureContainer(unittest.TestCase):
    @parameterized.expand([
        [3202, [0, 3, 2, 2]],
        [1, [0, 0, 0, 1]],
        [12345, [1, 2, 3, 45]],
    ])
    def test_opcode_splitter(self, code, result):
        self.assertListEqual(read_opcode(code), result)

    @parameterized.expand([
        [[1], 15314507],
        [[5], 652726],
    ])
    def test_final_results(self, start_value, result):
        self.assertEqual(run_intcode_program(puzzle_input.copy(), start_value, show_output=False)[0][-1], result)


if __name__ == '__main__':
    print(">>> Start Main 05:")
    run_intcode_program(puzzle_input.copy(), [1], show_output=True)
    run_intcode_program(puzzle_input.copy(), [5], show_output=True)
    print("End Main 05<<<")
