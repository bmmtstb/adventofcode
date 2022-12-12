import unittest
from typing import Dict, List, Tuple, Set, Union

from helper.file import read_lines_as_list

Order = Tuple[str, Union[int, None]]
Program = List[Order]


def execute_program(program: Program) -> List[int]:
    """execute the program and return the signal strength on every cycle as list"""
    def process_cycle(count, value) -> int:
        count += 1
        # calculate signal strength
        signals.append(count * value)
        return count

    register_value: int = 1
    cycle_count: int = 0
    signals: List[int] = [0]
    for order in program:
        if order[0] == "noop":
            cycle_count = process_cycle(cycle_count, register_value)
        elif order[0] == "addx":
            cycle_count = process_cycle(cycle_count, register_value)
            cycle_count = process_cycle(cycle_count, register_value)
            register_value += int(order[1])
        else:
            raise Exception(f"Invalid order: {order}")

    return signals


def evaluate_signal_strengths(signals: List[int]) -> int:
    """sum of every signal at 20 + 40n"""
    return sum(signals[i] for i in range(20, len(signals), 40))


def draw_crt_screen(signals: List[int]) -> str:
    """draw the crt screen"""
    width = 40
    screen = "\n"
    # first signal is dummy value
    for pixel_idx, signal in enumerate(signals[1:], start=0):
        # recalculate value by dividing signal by cycle count (here index of the current pixel)
        sprite_center_position = (signal // (pixel_idx + 1)) % width
        screen += "#" if pixel_idx % width - 1 <= sprite_center_position <= pixel_idx % width + 1 else "."
        if (pixel_idx + 1) % width == 0:
            screen += "\n"
    return screen


class Test2022Day10(unittest.TestCase):
    test_program = read_lines_as_list("data/10-test.txt", split=" ")
    test_signals = execute_program(test_program)
    test_crt_screen = "\n" \
        "##..##..##..##..##..##..##..##..##..##..\n" \
        "###...###...###...###...###...###...###.\n" \
        "####....####....####....####....####....\n" \
        "#####.....#####.....#####.....#####.....\n" \
        "######......######......######......####\n" \
        "#######.......#######.......#######.....\n"

    def test_execute_program(self):
        for i, value in [
            (20, 420),
            (60, 1140),
            (100, 1800),
            (140, 2940),
            (180, 2880),
            (220, 3960),
        ]:
            with self.subTest(msg=f'iteration: {i}, value: {value}'):
                self.assertEqual(self.test_signals[i], value)

    def test_evaluate_signal_strengths(self):
        self.assertEqual(evaluate_signal_strengths(self.test_signals), 13140)

    def test_draw_crt_screen(self):
        self.assertEqual(draw_crt_screen(self.test_signals), self.test_crt_screen)


if __name__ == '__main__':
    print(">>> Start Main 10:")
    puzzle_input = read_lines_as_list("data/10.txt", split=" ")
    puzzle_signals = execute_program(puzzle_input)
    print("Part 1): ", evaluate_signal_strengths(puzzle_signals))
    print("Part 2): ", "\n", draw_crt_screen(puzzle_signals))
    print("End Main 10<<<")
