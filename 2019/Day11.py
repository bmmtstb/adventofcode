import unittest

from Day05 import run_intcode_program

puzzle_input = [3, 8, 1005, 8, 311, 1106, 0, 11, 0, 0, 0, 104, 1, 104, 0, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10,
                108, 0, 8, 10, 4, 10, 102, 1, 8, 28, 1, 1104, 0, 10, 1006, 0, 71, 2, 1002, 5, 10, 2, 1008, 5, 10, 3, 8,
                1002, 8, -1, 10, 1001, 10, 1, 10, 4, 10, 1008, 8, 0, 10, 4, 10, 102, 1, 8, 66, 3, 8, 1002, 8, -1, 10,
                101, 1, 10, 10, 4, 10, 108, 1, 8, 10, 4, 10, 102, 1, 8, 87, 1006, 0, 97, 2, 1002, 6, 10, 3, 8, 102, -1,
                8, 10, 1001, 10, 1, 10, 4, 10, 108, 0, 8, 10, 4, 10, 102, 1, 8, 116, 1006, 0, 95, 1, 1009, 10, 10, 3, 8,
                102, -1, 8, 10, 101, 1, 10, 10, 4, 10, 108, 1, 8, 10, 4, 10, 102, 1, 8, 145, 1, 1002, 19, 10, 2, 1109,
                7, 10, 1006, 0, 18, 3, 8, 1002, 8, -1, 10, 101, 1, 10, 10, 4, 10, 1008, 8, 1, 10, 4, 10, 1001, 8, 0,
                179, 3, 8, 102, -1, 8, 10, 101, 1, 10, 10, 4, 10, 108, 0, 8, 10, 4, 10, 102, 1, 8, 200, 1, 1105, 14, 10,
                1, 1109, 14, 10, 2, 1109, 11, 10, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 1008, 8, 1, 10, 4, 10,
                102, 1, 8, 235, 3, 8, 1002, 8, -1, 10, 1001, 10, 1, 10, 4, 10, 1008, 8, 1, 10, 4, 10, 1002, 8, 1, 257,
                2, 101, 9, 10, 3, 8, 1002, 8, -1, 10, 101, 1, 10, 10, 4, 10, 108, 0, 8, 10, 4, 10, 101, 0, 8, 282, 2,
                1109, 19, 10, 1, 105, 0, 10, 101, 1, 9, 9, 1007, 9, 1033, 10, 1005, 10, 15, 99, 109, 633, 104, 0, 104,
                1, 21102, 937268368140, 1, 1, 21102, 328, 1, 0, 1106, 0, 432, 21102, 1, 932700599052, 1, 21101, 0, 339,
                0, 1105, 1, 432, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0,
                104, 1, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 1, 21101, 0, 209421601831, 1, 21102, 1, 386, 0, 1106,
                0, 432, 21102, 235173604443, 1, 1, 21102, 1, 397, 0, 1106, 0, 432, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0,
                104, 0, 21101, 825439855372, 0, 1, 21102, 1, 420, 0, 1106, 0, 432, 21101, 0, 988220907880, 1, 21102,
                431, 1, 0, 1106, 0, 432, 99, 109, 2, 22101, 0, -1, 1, 21101, 40, 0, 2, 21102, 1, 463, 3, 21102, 453, 1,
                0, 1106, 0, 496, 109, -2, 2105, 1, 0, 0, 1, 0, 0, 1, 109, 2, 3, 10, 204, -1, 1001, 458, 459, 474, 4, 0,
                1001, 458, 1, 458, 108, 4, 458, 10, 1006, 10, 490, 1102, 1, 0, 458, 109, -2, 2106, 0, 0, 0, 109, 4,
                2102, 1, -1, 495, 1207, -3, 0, 10, 1006, 10, 513, 21102, 0, 1, -3, 22102, 1, -3, 1, 21202, -2, 1, 2,
                21102, 1, 1, 3, 21101, 532, 0, 0, 1105, 1, 537, 109, -4, 2105, 1, 0, 109, 5, 1207, -3, 1, 10, 1006, 10,
                560, 2207, -4, -2, 10, 1006, 10, 560, 21201, -4, 0, -4, 1106, 0, 628, 22102, 1, -4, 1, 21201, -3, -1, 2,
                21202, -2, 2, 3, 21102, 1, 579, 0, 1106, 0, 537, 21202, 1, 1, -4, 21102, 1, 1, -1, 2207, -4, -2, 10,
                1006, 10, 598, 21101, 0, 0, -1, 22202, -2, -1, -2, 2107, 0, -3, 10, 1006, 10, 620, 21201, -1, 0, 1,
                21102, 1, 620, 0, 105, 1, 495, 21202, -2, -1, -2, 22201, -4, -2, -4, 109, -5, 2105, 1, 0]


class Robot:
    def __init__(self, intcode: list, input_values=None, input_painted=None, draw=False):
        self.input = [] if input_values is None else list(input_values)
        self.intcode = intcode.copy()
        self.code_pointer = 0
        self.code_relative_base = 0
        self.facing = (0, -1)  # up
        self.position = (0, 0)
        # tuple of painted panels and their respective color (possible duplicates - ordered)
        self.painted = [] if input_painted is None else list(input_painted)
        self.draw_final = draw

    def run(self):
        """run the robot"""
        finished = False
        while not finished:
            current_color = self.detect_color(self.position)
            self.input.append(current_color)
            output, finished = self.run_intcode_program()
            if finished:
                if self.draw_final:
                    self.draw()
                return self.get_nof_painted()
            if len(output) != 2:
                raise Exception("Output should have length two but the output was: {}".format(output))
            # paint the hull using the first output
            self.paint(self.position, output[0])
            # move the robot according to the second output
            self.move(output[1])


    def run_intcode_program(self):
        """run the program with current state until further input is needed"""
        out, pointer, relative_base, code = run_intcode_program(self.intcode, self.input, pointer_start=self.code_pointer,relative_base_start=self.code_relative_base)
        self.input = []  # reset input
        self.code_pointer = pointer
        self.code_relative_base = relative_base
        self.intcode = code
        return out, pointer is None

    def move(self, turn_direction):
        """turn in given direction, then step forward 1 tile"""
        # turn_direction (0: 90° Left, 1: 90° right)
        if turn_direction == 0:
            self.facing = (self.facing[1], -self.facing[0])
        elif turn_direction == 1:
            self.facing = (-self.facing[1], self.facing[0])
        else:
            raise Exception("Invalid turn direction {}".format(turn_direction))
        # step forward
        self.position = (self.position[0] + self.facing[0], self.position[1] + self.facing[1])

    def paint(self, position, color):
        """Paint one panel"""
        self.painted.append((position, color))

    def detect_color(self, position):
        """return color of given position """
        # initially all panels are black -> if not painted yet panel is black
        #  black: 0 ; white: 1
        painted = list(filter(lambda x: x[0] == position, self.painted))
        return painted[-1][1] if len(painted) else 0

    def get_nof_painted(self):
        """return number of unique painted panels"""
        return len(set([x[0] for x in self.painted]))

    def draw(self):
        """draw the current image"""
        final_color_values = {}
        area_limits = ((0, 0), (0, 0))  # ((x_min, y_min), (x_max, y_max))
        for value in reversed(self.painted):
            if not (value in final_color_values.keys()):
                final_color_values[value[0]] = value[1]
                # change area limits if necessary
                area_limits = (
                    (min(area_limits[0][0], value[0][0]), min(area_limits[0][1], value[0][1])),  # min
                    (max(area_limits[1][0], value[0][0]), max(area_limits[1][1], value[0][1]))  # max
                )
        # init nested array of correct size with all values black
        color_array = [[0]*(area_limits[1][0] - area_limits[0][0] + 1) for _ in range(area_limits[1][1] - area_limits[0][1] + 1)]
        # add values to array
        for tile in final_color_values.keys():
            color_array[tile[1] - area_limits[0][1]][tile[0] - area_limits[0][0]] = final_color_values[tile]
        # print results
        for row in color_array:
            print(''.join('#' if value == 1 else ' ' for value in row))


class Test2019Day11(unittest.TestCase):
    # Tests not feasible
    pass


if __name__ == '__main__':
    print(">>> Start Main 11:")
    print("Part 1):")
    hull_painting_robot_1 = Robot(puzzle_input.copy())
    print(hull_painting_robot_1.run())
    print("Part 2):")
    hull_painting_robot_2 = Robot(puzzle_input.copy(), input_painted=[((0, 0), 1)], draw=True)
    print(hull_painting_robot_2.run())
    print("End Main 11<<<")
