# opcode (code, a, b, pos)
# 1: add: pos = a + b
# 2: mult: pos = a * b
# 99: end

import unittest

from parameterized import parameterized

global_intcode = [1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 10, 19, 1, 19, 6, 23, 2, 23, 13, 27, 1, 27, 5,
                  31, 2, 31, 10, 35, 1, 9, 35, 39, 1, 39, 9, 43, 2, 9, 43, 47, 1, 5, 47, 51, 2, 13, 51, 55, 1, 55, 9, 59,
                  2, 6, 59, 63, 1, 63, 5, 67, 1, 10, 67, 71, 1, 71, 10, 75, 2, 75, 13, 79, 2, 79, 13, 83, 1, 5, 83, 87,
                  1, 87, 6, 91, 2, 91, 13, 95, 1, 5, 95, 99, 1, 99, 2, 103, 1, 103, 6, 0, 99, 2, 14, 0, 0]


def run_intcode_program(intcode):
    """Calculate final intcode sequence"""
    instruction_pointer = 0
    opcode = intcode[instruction_pointer]
    while opcode != 99:
        if opcode == 1:
            intcode[intcode[instruction_pointer + 3]] = intcode[intcode[instruction_pointer + 1]] + intcode[intcode[instruction_pointer + 2]]
        elif opcode == 2:
            intcode[intcode[instruction_pointer + 3]] = intcode[intcode[instruction_pointer + 1]] * intcode[intcode[instruction_pointer + 2]]
        else:
            raise ValueError("Something went wrong, opcode {} is not expected.".format(opcode))
        instruction_pointer += 4
        opcode = intcode[instruction_pointer]
    return intcode, intcode[0]


def find_intcode_inputs(input_intcode, input_addresses, input_range, wished_output):
    """
    For a list of input addresses, each with a specific input range, find a given output
    :param input_intcode: intcode program as list, may not be changed
    :param input_addresses: list of input addresses to change
    :param input_range: list of tuples, one 2D-tuple for each input address
    :param wished_output: wished output at pos[0]
    """
    def set_new_intcode(saved_code, address, value):
        """Set a new intcode value at specified address, old intcode should not change"""
        new_intcode = saved_code.copy()
        new_intcode[address] = value
        return new_intcode

    if len(input_addresses) > 1:
        for i in range(*input_range[0]):
            result = find_intcode_inputs(set_new_intcode(input_intcode, input_addresses[0], i), input_addresses[1:], input_range[1:], wished_output)
            if result:
                result.insert(0, i)
                return result
        return None
    else:
        for j in range(*input_range[0]):
            try:
                _, output = run_intcode_program(set_new_intcode(input_intcode, input_addresses[0], j))
                if output == wished_output:
                    return [j]
            except ValueError:
                pass
            except IndexError:
                pass
        return None


class TestIntcode(unittest.TestCase):
    @parameterized.expand([
        ["null", [99], [99]],
        ["Addition", [1, 0, 0, 0, 99], [2, 0, 0, 0, 99]],
        ["Multiplication", [2, 3, 0, 3, 99], [2, 3, 0, 6, 99]],
        ["Trailing 0", [2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]],
        ["removed 99", [1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]],
        ["multistep", [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]],
    ])
    def testBasicIntcode(self, name, code, result):
        code_result, _ = run_intcode_program(code)
        self.assertEqual(code_result, result, msg="Test {} failed.".format(name))

    @parameterized.expand([
        [[1, 0, 0, 0, 99], [1, 2], [(0, 99), (0, 99)], 2, [0, 0]],
        [[1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], [1, 2], [(0, 99), (0, 99)], 3500, [9, 10]],
    ])
    def testFindOutput(self, i_code, i_addresses, i_range, output, result):
        self.assertEqual(find_intcode_inputs(i_code, i_addresses, i_range, output), result)


if __name__ == '__main__':
    # make sure to use unique memory for every test
    # before running the program, replace position 1 with the value 12 and replace position 2 with the value 2.
    # What value is left at position 0 after the program halts?
    memory1 = global_intcode.copy()
    memory1[1] = 12  # noun
    memory1[2] = 2  # verb
    result1, output1 = run_intcode_program(memory1)
    print(result1)
    print("Pos 0: ", output1)

    # find a pair of inputs that produce output 19690720
    memory2 = global_intcode.copy()
    result2 = find_intcode_inputs(memory2, [1, 2], [(0, 99), (0, 99)], 19690720)
    print("100 * noun + verb: ", 100 * result2[0] + result2[1])
