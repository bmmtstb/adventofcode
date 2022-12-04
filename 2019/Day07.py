import unittest
from itertools import permutations

from Day05 import run_intcode_program

puzzle_input = [3, 8, 1001, 8, 10, 8, 105, 1, 0, 0, 21, 46, 55, 72, 85, 110, 191, 272, 353, 434, 99999, 3, 9, 1002, 9,
                5, 9, 1001, 9, 2, 9, 102, 3, 9, 9, 101, 2, 9, 9, 102, 4, 9, 9, 4, 9, 99, 3, 9, 102, 5, 9, 9, 4, 9, 99,
                3, 9, 1002, 9, 2, 9, 101, 2, 9, 9, 1002, 9, 2, 9, 4, 9, 99, 3, 9, 1002, 9, 4, 9, 101, 3, 9, 9, 4, 9, 99,
                3, 9, 1002, 9, 3, 9, 101, 5, 9, 9, 1002, 9, 3, 9, 101, 3, 9, 9, 1002, 9, 5, 9, 4, 9, 99, 3, 9, 1001, 9,
                2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 102, 2,
                9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2,
                9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 99, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9,
                1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3,
                9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9,
                99, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9,
                4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 2,
                9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 99, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 102,
                2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9,
                1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3,
                9, 1001, 9, 1, 9, 4, 9, 99, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4,
                9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9,
                4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 99]


def get_amplification_score(program, sequence) -> int:
    """
    Get the final score of connected amplifiers
    :param program: intcode program
    :param sequence: current sequence to test the output of
    :return: value of the last amplifier
    """
    signal = 0
    for phase_value in sequence:
        out, _, _, _ = run_intcode_program(intcode=program.copy(), program_input=[phase_value, signal], show_output=False)
        signal = out[-1]
    return signal


def get_feedback_loop_score(amp_input: list, sequence: tuple) -> int:
    """
    Get the final score of amplifiers connected via a feedback loop
    :param amp_input: intcode program
    :param sequence: current sequence to test the output of
    :return: value of the last amplifier at the end of the loop
    """
    signal = 0
    amplifiers = [{"in": [], "out": [], "pointer": 0, "code": amp_input.copy()} for _ in range(len(sequence))]
    # add init conditions
    for j, amp in enumerate(amplifiers):
        amp["in"].append(sequence[j])
    # input first signal
    amplifiers[0]["in"].append(signal)

    # run loop until last pointer points to none
    i_amp = 0
    while amplifiers[-1]["pointer"] is not None:
        # get current and last amplifier
        curr_amp = amplifiers[i_amp]
        last_amp = amplifiers[(i_amp + 4) % 5]
        # add output of last amplifier to current input and remove it from last amp
        curr_amp["in"] += last_amp["out"]
        last_amp["out"] = []
        # run next amplifier
        new_out, new_pointer, _, new_code = run_intcode_program(
            intcode=curr_amp["code"],
            program_input=curr_amp["in"],
            pointer_start=curr_amp["pointer"]
        )

        # update current amplifier with updated values
        curr_amp["out"] += new_out
        curr_amp["pointer"] = new_pointer
        curr_amp["new_code"] = new_code

        # increase pointer
        i_amp = (i_amp + 1) % 5
    # return the las value of the last amp
    return amplifiers[-1]["out"][-1]


def find_amplifying_sequence(amp_input, list_of_amps: list, feedback_loop: bool = False) -> (list, int):
    """
    Calculate the best amplifying sequence and highest returning value given an intcode program
    :param amp_input: intcode program
    :param list_of_amps: number of amplifiers used (0-4 -> 5 pc)
    :param feedback_loop: whether or not to interpret the amplifiers as feedback loop
    :return: phase setting sequence with highest output
    """
    combinations = list(permutations(list_of_amps))
    best = 0
    best_sequence = ()
    for combination in combinations:
        if feedback_loop:
            score = get_feedback_loop_score(amp_input.copy(), combination)
        else:
            score = get_amplification_score(amp_input.copy(), combination)
        # update best value and sequence
        if score > best:
            best = score
            best_sequence = combination
    return best_sequence, best


class Test2019Day07(unittest.TestCase):
    def test_find_sequence(self):
        for int_code, final_sequence, max_signal in [
            [[3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0], (4, 3, 2, 1, 0), 43210],
            [[3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0],
             (0, 1, 2, 3, 4), 54321],
            [[3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32,
              31,
              31, 4, 31, 99, 0, 0, 0], (1, 0, 4, 3, 2), 65210]
        ]:
            with self.subTest():
                seq, score = find_amplifying_sequence(int_code, [0, 1, 2, 3, 4])
                self.assertEqual(seq, final_sequence)
                self.assertEqual(score, max_signal)

    def test_find_feedback_loop_sequence(self):
        for int_code, final_sequence, max_signal in [
            [[3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99,
              0,
              0, 5], (9, 8, 7, 6, 5), 139629729],
            [[3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1,
              12,
              1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005, 56, 6, 99,
              0,
              0, 0, 0, 10], (9, 7, 8, 5, 6), 18216],
        ]:
            with self.subTest():
                seq, score = find_amplifying_sequence(int_code, [5, 6, 7, 8, 9], feedback_loop=True)
                self.assertEqual(seq, final_sequence)
                self.assertEqual(score, max_signal)


if __name__ == '__main__':
    print("Start Main 07:")
    best_seq, best_value = find_amplifying_sequence(puzzle_input.copy(), [0, 1, 2, 3, 4])
    print("1) Best Sequence was {} with a value of {}".format(best_seq, best_value))
    best_seq, best_value = find_amplifying_sequence(puzzle_input.copy(), [5, 6, 7, 8, 9], feedback_loop=True)
    print("2) Best Sequence was {} with a value of {}".format(best_seq, best_value))
    print("End Main 07")
