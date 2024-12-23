import unittest
from copy import deepcopy

from helper.file import load_file_and_split
from helper.tuple import tuple_add_tuple

Position = tuple[int, int]
Map = list[list[str]]


directions: dict[str, Position] = {
    "^": (-1, 0),
    "v": (1, 0),
    ">": (0, 1),
    "<": (0, -1),
}


def load_data(fp: str) -> tuple[Map, list[Position]]:
    """Get the map and the moves from the file."""
    map_, moves = load_file_and_split(fp, "\n\n")
    return [list(row) for row in map_.split("\n")], [directions[move] for move in moves]


def load_scaled_up_data(fp: str) -> tuple[Map, list[Position]]:
    """Get the scaled up map and the moves from the file."""
    map_, moves = load_file_and_split(fp, "\n\n")
    large_map: Map = []
    for row in map_.split("\n"):
        large_row = []
        for char in row:
            if char == "#":
                large_row += ["#", "#"]
            elif char == "O":
                large_row += ["[", "]"]
            elif char == ".":
                large_row += [".", "."]
            elif char == "@":
                large_row += ["@", "."]
            else:
                raise NotImplementedError(f"Got undefined char {char}")
        large_map += [large_row]
    return large_map, [directions[move] for move in moves]


def get_gps_score(map_: Map) -> int:
    """Given the map, find all boxes and return the cumulative GPS score."""
    total = 0
    for i, row in enumerate(map_):
        for j, char in enumerate(row):
            if char in ["O", "["]:
                total += 100 * i + j
    return total


def find_player_and_remove_map(m: Map) -> tuple[Position, Map]:
    """Find the player position and remove it from the map."""
    for i, row in enumerate(m):
        if "@" in row:
            j = row.index("@")
            # replace '@' with '.' to remove redundant information of the current position
            m[i][j] = "."
            return (i, j), m
    raise NotImplementedError("Could not find the player position.")


def run_small_simulation(m: Map, moves: list[Position]) -> Map:
    """Rune every step of the simulation on a small map."""
    m = deepcopy(m)

    curr_pos, m = find_player_and_remove_map(m)

    for move in moves:
        new_pos = tuple_add_tuple(curr_pos, move)

        if 0 > new_pos[0] >= len(m) or 0 > new_pos[1] >= len(m[0]):
            continue

        new_tile = m[new_pos[0]][new_pos[1]]

        # move to an empty space
        if new_tile == ".":
            curr_pos = new_pos
            continue
        # bump into a wall
        if new_tile == "#":
            continue
        # move to a box
        if new_tile == "O":
            new_box_pos = tuple_add_tuple(new_pos, move)
            while True:
                new_box_pos_tile = m[new_box_pos[0]][new_box_pos[1]]

                if new_box_pos_tile == "#":
                    break
                if new_box_pos_tile == ".":
                    m[new_box_pos[0]][new_box_pos[1]] = "O"
                    m[new_pos[0]][new_pos[1]] = "."
                    curr_pos = new_pos
                    break
                if new_box_pos_tile == "O":
                    new_box_pos = tuple_add_tuple(new_box_pos, move)
                    continue
                assert False, f"Got undefined tile {new_box_pos_tile} while moving box"
            continue
        assert False, f"Got undefined tile {new_tile}"

    return m


def run_large_simulation(m: Map, moves: list[Position]) -> Map:
    """Rune every step of the simulation on the large map."""
    # I'm sorry, this is a mess...
    # pylint: disable=too-many-branches,too-many-locals,too-many-nested-blocks,too-many-statements

    m = deepcopy(m)
    curr_pos, m = find_player_and_remove_map(m)

    for move in moves:
        new_pos = tuple_add_tuple(curr_pos, move)

        if 0 > new_pos[0] >= len(m) or 0 > new_pos[1] >= len(m[0]):
            raise NotImplementedError(f"Out of bounds move {new_pos}")

        new_tile = m[new_pos[0]][new_pos[1]]

        # move to an empty space
        if new_tile == ".":
            curr_pos = new_pos
            continue
        # bump into a wall
        if new_tile == "#":
            continue
        # move to a box
        if new_tile in ["[", "]"]:
            new_box_pos = tuple_add_tuple(new_pos, move)

            # a horizontal move can only push a line of boxes as before
            # (without splitting left right like with vertical moves)
            if move[0] == 0:
                while True:
                    new_box_pos_tile = m[new_box_pos[0]][new_box_pos[1]]

                    if new_box_pos_tile == "#":
                        break
                    if new_box_pos_tile == ".":
                        for count, idx in enumerate(range(new_box_pos[1], new_pos[1], -1 * move[1])):
                            if (count % 2 == 0 and move[1] == -1) or (count % 2 != 0 and move[1] == 1):
                                m[new_box_pos[0]][idx] = "["
                            else:
                                m[new_box_pos[0]][idx] = "]"

                        m[new_pos[0]][new_pos[1]] = "."
                        curr_pos = new_pos
                        break
                    if new_box_pos_tile in ["[", "]"]:
                        new_box_pos = tuple_add_tuple(new_box_pos, move)
                        continue
                    assert False, f"Got undefined tile {new_box_pos_tile} while moving box"
                continue

            # vertical moves can push multiple boxes
            # first add the initial box to the set of boxes to analyze
            boxes_to_analyze = {new_pos}
            if m[new_pos[0]][new_pos[1]] == "[":
                boxes_to_analyze.add(tuple_add_tuple(new_pos, (0, 1)))
            elif m[new_pos[0]][new_pos[1]] == "]":
                boxes_to_analyze.add(tuple_add_tuple(new_pos, (0, -1)))
            else:
                raise NotImplementedError(f"Got undefined tile {m[new_pos[0]][new_pos[1]]}")

            analyzed_boxes = set()

            while len(boxes_to_analyze) > 0:
                # get a box from the stack
                analyzed_box_pos = boxes_to_analyze.pop()
                analyzed_box_tile = m[analyzed_box_pos[0]][analyzed_box_pos[1]]

                # analyze the box
                if 0 > analyzed_box_pos[0] >= len(m) or 0 > analyzed_box_pos[1] >= len(m[0]):
                    boxes_to_analyze.add("dummy")
                    break
                if analyzed_box_tile == "#":
                    boxes_to_analyze.add("dummy")
                    break

                if analyzed_box_tile == ".":  # the box can be moved, but moving will be done later
                    continue

                # the next tile won't break the loop and has to be modified, so add the box to the analyzed set
                analyzed_boxes.add(analyzed_box_pos)

                if analyzed_box_tile == "[":
                    # add the right box, if it has not been analyzed yet
                    if (right_box := tuple_add_tuple(analyzed_box_pos, (0, 1))) not in analyzed_boxes:
                        boxes_to_analyze.add(right_box)
                    # add the right two boxes above (or below) this part of the box to the stack
                    boxes_to_analyze.add(tuple_add_tuple(analyzed_box_pos, (move[0], 0)))
                    # boxes_to_analyze.add(tuple_add_tuple(analyzed_box_pos, (move[0], 1)))
                    continue
                if analyzed_box_tile == "]":
                    # add the left box, if it has not been analyzed yet
                    if (left_box := tuple_add_tuple(analyzed_box_pos, (0, -1))) not in analyzed_boxes:
                        boxes_to_analyze.add(left_box)

                    # add the left two boxes above (or below) this part of the box to the stack
                    boxes_to_analyze.add(tuple_add_tuple(analyzed_box_pos, (move[0], 0)))
                    # boxes_to_analyze.add(tuple_add_tuple(analyzed_box_pos, (move[0], -1)))
                    continue

            # move all boxes iff all boxes can be moved
            if len(boxes_to_analyze) == 0 and len(analyzed_boxes) > 0:
                new_map = deepcopy(m)
                # first, clear the old positions in the new copy to make sure that moved boxes are removed correctly
                for box in analyzed_boxes:
                    new_map[box[0]][box[1]] = "."

                # secondly, actually move the boxes from the old to the new position
                for box in analyzed_boxes:
                    new_analyzed_box_pos = tuple_add_tuple(box, move)
                    new_map[new_analyzed_box_pos[0]][new_analyzed_box_pos[1]] = m[box[0]][box[1]]

                # finally, update the current map and position
                m = new_map
                curr_pos = new_pos
                continue
            # continue with the next move even, if not all the boxes can be moved
            continue

        assert False, f"Got undefined tile {new_tile}"

    return m


def part1(m: Map, moves: list[Position]) -> int:
    """Part1: Run the simulation and return the GPS score."""
    final_map = run_small_simulation(m, moves)
    return get_gps_score(final_map)


def part2(m: Map, moves: list[Position]) -> int:
    """Part2: Run the simulation on the large map and return the GPS score."""
    final_map = run_large_simulation(m, moves)
    return get_gps_score(final_map)


class Test2024Day15(unittest.TestCase):

    fp = "./data/15-test.txt"
    test_data = load_data(fp)
    test_data_large = load_scaled_up_data(fp)

    final_map: Map = [
        ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
        ["#", ".", "O", ".", "O", ".", "O", "O", "O", "#"],
        ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
        ["#", "O", "O", ".", ".", ".", ".", ".", ".", "#"],
        ["#", "O", "O", "@", ".", ".", ".", ".", ".", "#"],
        ["#", "O", "#", ".", ".", ".", ".", ".", "O", "#"],
        ["#", "O", ".", ".", ".", ".", ".", "O", "O", "#"],
        ["#", "O", ".", ".", ".", ".", ".", "O", "O", "#"],
        ["#", "O", "O", ".", ".", ".", ".", "O", "O", "#"],
        ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ]
    final_map_large: Map = [
        ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
        ["#", "#", "[", "]", ".", ".", ".", ".", ".", ".", ".", "[", "]", ".", "[", "]", "[", "]", "#", "#"],
        ["#", "#", "[", "]", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "[", "]", ".", "#", "#"],
        ["#", "#", "[", "]", ".", ".", ".", ".", ".", ".", ".", ".", "[", "]", "[", "]", "[", "]", "#", "#"],
        ["#", "#", "[", "]", ".", ".", ".", ".", ".", ".", "[", "]", ".", ".", ".", ".", "[", "]", "#", "#"],
        ["#", "#", ".", ".", "#", "#", ".", ".", ".", ".", ".", ".", "[", "]", ".", ".", ".", ".", "#", "#"],
        ["#", "#", ".", ".", "[", "]", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "#"],
        ["#", "#", ".", ".", "@", ".", ".", ".", ".", ".", ".", "[", "]", ".", "[", "]", "[", "]", "#", "#"],
        ["#", "#", ".", ".", ".", ".", ".", ".", "[", "]", "[", "]", ".", ".", "[", "]", ".", ".", "#", "#"],
        ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ]

    fp_short = "./data/15-test-short.txt"
    test_data_short = load_data(fp_short)
    final_map_short: Map = [
        ["#", "#", "#", "#", "#", "#", "#", "#"],
        ["#", ".", ".", ".", ".", "O", "O", "#"],
        ["#", "#", ".", ".", ".", ".", ".", "#"],
        ["#", ".", ".", ".", ".", ".", "O", "#"],
        ["#", ".", "#", "O", "@", ".", ".", "#"],
        ["#", ".", ".", ".", "O", ".", ".", "#"],
        ["#", ".", ".", ".", "O", ".", ".", "#"],
        ["#", "#", "#", "#", "#", "#", "#", "#"],
    ]

    fp_t2 = "./data/15-test-2.txt"
    test_data_p2 = load_scaled_up_data(fp_t2)
    final_map_p2: Map = [
        ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
        ["#", "#", ".", ".", ".", "[", "]", ".", "#", "#", ".", ".", "#", "#"],
        ["#", "#", ".", ".", ".", "@", ".", "[", "]", ".", ".", ".", "#", "#"],
        ["#", "#", ".", ".", ".", ".", "[", "]", ".", ".", ".", ".", "#", "#"],
        ["#", "#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "#"],
        ["#", "#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", "#"],
        ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ]

    def test_p1_short(self):
        self.assertEqual(part1(*self.test_data_short), 2028)

    def test_p1(self):
        self.assertEqual(part1(*self.test_data), 10092)

    def test_p2(self):
        self.assertEqual(part2(*self.test_data_large), 9021)

    def test_p2_short(self):
        self.assertEqual(part2(*self.test_data_p2), 105 + 207 + 306)

    def test_gps_score(self):
        for name, map_, score in [
            ("regular", self.final_map, 10092),
            ("large", self.final_map_large, 9021),
            ("short", self.final_map_short, 2028),
            ("p2", self.final_map_p2, 105 + 207 + 306),
        ]:
            with self.subTest(msg="name: {}, map: {}, score: {}".format(name, map_, score)):
                self.assertEqual(get_gps_score(map_), score)


if __name__ == "__main__":
    print(">>> Start Main 15:")
    print("Part 1): ", part1(*load_data("./data/15.txt")))
    print("Part 2): ", part2(*load_scaled_up_data("./data/15.txt")))
    print("End Main 15<<<")
