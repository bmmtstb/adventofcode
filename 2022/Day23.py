import unittest
from copy import deepcopy
from typing import Dict, List, Tuple, Set

from helper.file import read_lines_as_list
from helper.tuple import tuple_add_tuple

ElfPosition = Tuple[int, int]
ElvesPositions = List[ElfPosition]

MOVE_DIRECTION: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]] = (
    (0, -1),  # N
    (0, 1),  # S
    (-1, 0),  # W
    (1, 0),  # E
)


class Elves:
    def __init__(self, starting_pos: List[List[str]]):
        self.elves: ElvesPositions = []
        # get list of elf positions from rows and cols
        for y, row in enumerate(starting_pos):
            for x, symbol in enumerate(row):
                if symbol == "#":
                    self.elves.append((x, y))

    def has_any_neighbors_in_direction(self, pos: ElfPosition, direction: int) -> bool:
        """get neighbors of elf in N,S,W,E direction"""
        if direction == 0:
            return any(
                other_elf[1] == pos[1] - 1 and
                pos[0] - 1 <= other_elf[0] <= pos[0] + 1
                for other_elf in self.elves if pos is not other_elf
            )
        elif direction == 1:
            return any(
                other_elf[1] == pos[1] + 1 and
                pos[0] - 1 <= other_elf[0] <= pos[0] + 1
                for other_elf in self.elves if pos is not other_elf
            )
        elif direction == 2:
            return any(
                other_elf[0] == pos[0] - 1 and
                pos[1] - 1 <= other_elf[1] <= pos[1] + 1
                for other_elf in self.elves if pos is not other_elf
            )
        elif direction == 3:
            return any(
                other_elf[0] == pos[0] + 1 and
                pos[1] - 1 <= other_elf[1] <= pos[1] + 1
                for other_elf in self.elves if pos is not other_elf
            )
        raise Exception(f'Invalid direction {dir}')

    def has_at_least_one_neighbor(self, pos: ElfPosition) -> bool:
        """return whether pos has at least one neighboring elf"""
        return any(pos[0] - 1 <= other_elf[0] <= pos[0] + 1 and
                   pos[1] - 1 <= other_elf[1] <= pos[1] + 1
                   for other_elf in self.elves if other_elf != pos)

    def has_neighbors_in_dir(self, pos: ElfPosition) -> Tuple[bool, bool, bool, bool]:
        """return whether there is at least one N,S,W,E neighbor"""
        N, S, W, E = False, False, False, False
        for other_elf in self.elves:
            if not N and other_elf[1] == pos[1] - 1 and pos[0] - 1 <= other_elf[0] <= pos[0] + 1:
                N = True
            if not S and other_elf[1] == pos[1] + 1 and pos[0] - 1 <= other_elf[0] <= pos[0] + 1:
                S = True
            if not W and other_elf[0] == pos[0] - 1 and pos[1] - 1 <= other_elf[1] <= pos[1] + 1:
                W = True
            if not E and other_elf[0] == pos[0] + 1 and pos[1] - 1 <= other_elf[1] <= pos[1] + 1:
                E = True
            if N == S == W == E == True:
                break
        return N, S, W, E

    def get_free_spaces_in_rectangle(self) -> int:
        """get the size of the minimal axis-parallel rectangle and calculate free spaces"""
        min_ = list(map(min, *self.elves))
        max_ = list(map(max, *self.elves))
        rect_size = (max_[0] - min_[0] + 1) * (max_[1] - min_[1] + 1)

        return rect_size - len(self.elves)

    def draw_board(self) -> str:
        """makes debugging easier, print the board"""
        min_ = list(map(min, *self.elves))
        max_ = list(map(max, *self.elves))
        img = ""
        for row_id in range(min_[1], max_[1] + 1):
            img += "".join("#" if (x, row_id) in self.elves else "." for x in range(min_[0], max_[0] + 1)) + "\n"
        return img

    def run_simulation(self, n: int = -1) -> int:
        """run simulation for n rounds, stops if no elf moved, sets self.elves to new positions"""
        iteration = 0
        while iteration != n:
            # FIRST HALF - calculate possible movement
            # reset new positions
            new_positions: ElvesPositions = []
            elves_moved = False
            offset = iteration % 4
            # calculate new position of every elf
            for elf in self.elves:
                neighbors = self.has_neighbors_in_dir(elf)
                # no neighbors around elf or neighbors everywhere for current elf
                if sum(neighbors) == 0 or sum(neighbors) == 4:
                    new_positions.append(elf)
                    continue
                # at least one neighbor, not all neighbors
                for dir_i in range(0, 4):
                    # if no one in direction move to that direction, but directions keep changing based on offset
                    if not neighbors[(offset + dir_i) % 4]:
                        new_positions.append(tuple_add_tuple(elf, MOVE_DIRECTION[(offset + dir_i) % 4]))
                        elves_moved = True
                        break

            assert len(self.elves) == len(new_positions)

            # break loop if no elf moved
            if not elves_moved:
                return iteration + 1
            # SECOND HALF - move iff possible
            # update current positions, but if two elves go to the same position don't move them at all
            no_move_indices: List[int] = []
            for testing_index, new_pos in enumerate(new_positions):
                # can current elf move to new position
                current_can_move = True
                # skip already duplicates
                if testing_index in no_move_indices:
                    continue
                # loop over all following positions
                for other_idx, other_pos in enumerate(new_positions[testing_index + 1:], start=testing_index + 1):
                    # skip already duplicates
                    if other_idx in no_move_indices:
                        continue
                    # found duplicate
                    if new_pos == other_pos:
                        no_move_indices.append(other_idx)
                        current_can_move = False
                        # check all other points as well
                # current can't move
                if not current_can_move:
                    no_move_indices.append(testing_index)

            # reset all that do not move
            for no_move_index in no_move_indices:
                new_positions[no_move_index] = self.elves[no_move_index]

            assert len(self.elves) == len(new_positions)

            # update current positions after round
            self.elves = deepcopy(new_positions)
            # set elves value, are needed for neighbors

            # increase counter
            iteration += 1

        # completed, elves didn't change, return
        return iteration


class Test2022Day23(unittest.TestCase):
    test_elves = Elves(read_lines_as_list(filepath="data/23-test.txt", instance_type=str, split="every"))
    test_elves_small = Elves(read_lines_as_list(filepath="data/23-test-small.txt", instance_type=str, split="every"))
    test_elves_it1 = Elves(read_lines_as_list(filepath="data/23-test-it1.txt", instance_type=str, split="every"))

    def test_setup(self):
        self.assertEqual(deepcopy(self.test_elves_small.elves), [(2, 1), (3, 1), (2, 2), (2, 4), (3, 4)])

    def test_get_free_spaces_in_rectangle(self):
        self.assertEqual(deepcopy(self.test_elves_small).get_free_spaces_in_rectangle(), 3)
        self.assertEqual(deepcopy(self.test_elves).get_free_spaces_in_rectangle(), 27)

    def test_has_any_neighbors_in_direction(self):
        for elves, elf_pos, testing_direction, has_neighbors in [
            (deepcopy(self.test_elves_small), (0, 0), 1, False),
            (deepcopy(self.test_elves_small), (1, 1), 1, True),
            (deepcopy(self.test_elves_small), (1, 1), 2, False),
            (deepcopy(self.test_elves_small), (1, 1), 3, True),
            (deepcopy(self.test_elves_small), (3, 2), 0, True),
            (deepcopy(self.test_elves_small), (2, 2), 0, True),
            (deepcopy(self.test_elves_small), (2, 1), 0, False),
            (deepcopy(self.test_elves), (8, 4), 0, True),
            (deepcopy(self.test_elves), (8, 4), 1, True),
            (deepcopy(self.test_elves), (8, 4), 2, True),
            (deepcopy(self.test_elves), (8, 4), 3, True),
        ]:
            with self.subTest(msg=f'pos: {elf_pos}'):
                self.assertEqual(elves.has_any_neighbors_in_direction(elf_pos, testing_direction), has_neighbors)

    def test_has_at_least_one_neighbor(self):
        for elves, elf_pos, has_neighbors in [
            (deepcopy(self.test_elves_small), (0, 0), False),
            (deepcopy(self.test_elves_small), (1, 1), True),
            (deepcopy(self.test_elves_small), (1, 1), True),
            (deepcopy(self.test_elves_small), (3, 2), True),
            (deepcopy(self.test_elves_small), (2, 2), True),
            (deepcopy(self.test_elves_small), (2, 1), True),
            (deepcopy(self.test_elves), (8, 4), True),
            (deepcopy(self.test_elves), (5, 1), False),
            (deepcopy(self.test_elves_it1), (7, 1), False),
        ]:
            with self.subTest(msg=f'pos: {elf_pos}'):
                self.assertEqual(elves.has_at_least_one_neighbor(elf_pos), has_neighbors)

    def test_get_size_after_n_rounds(self):
        for elves, n, empty_spaces in [
            (deepcopy(self.test_elves_small), 1, 5),
            (deepcopy(self.test_elves_small), 2, 15),
            (deepcopy(self.test_elves_small), 10, 25),
            (deepcopy(self.test_elves), 10, 110),
        ]:
            with self.subTest(msg=f''):
                elves.run_simulation(n=n)
                self.assertEqual(elves.get_free_spaces_in_rectangle(), empty_spaces)

    def test_nof_iterations(self):
        self.assertEqual(deepcopy(self.test_elves).run_simulation(), 20)
        self.assertEqual(deepcopy(self.test_elves_small).run_simulation(), 4)


if __name__ == '__main__':
    print(">>> Start Main 23:")
    puzzle_input = Elves(read_lines_as_list(filepath="data/23.txt", instance_type=str, split="every"))
    p1 = deepcopy(puzzle_input)
    p2 = deepcopy(puzzle_input)
    p1.run_simulation(n=10)
    print("Part 1): ", p1.get_free_spaces_in_rectangle())
    print("Part 2): ", p2.run_simulation())  # don't resimulate p1
    # 916
    print("End Main 23<<<")
