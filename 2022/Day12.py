import unittest
from copy import deepcopy
from typing import Dict, List, Tuple, Set

import numpy as np

from helper.file import read_lines_as_list
from helper.tuple import tuple_add_tuple

Position = Tuple[int, int]


class PathFinder:
    """given a map evaluate it and find efficient paths"""

    def __init__(self, height_map: np.ndarray, skip_at: int = np.inf, g_value_init: np.ndarray = None):
        self.skip_at: int = skip_at
        self.height_map: np.ndarray = height_map
        self.height, self.width = self.height_map.shape
        self.start_pos: Position = tuple(int(x) for x in np.where(self.height_map == ord("S")))
        self.final_pos: Position = tuple(int(x) for x in np.where(self.height_map == ord("E")))
        # create f and g value map where the minimal cost of every node is stored
        # f: estimate path to goal from node
        self.f_value_map: np.ndarray = np.full(self.height_map.shape, np.inf, dtype=int)
        # g: cost to reach node
        self.g_value_map: np.ndarray = np.full(self.height_map.shape, self.width * self.height, dtype=int) if g_value_init is None else g_value_init
        # create a mapping where every (interesting) node points to the successor with the (current) minimal cost
        self.predecessor_map: Dict[Position, Position] = dict()
        # replace start and goal value
        self.height_map[self.start_pos] = ord("a")
        self.height_map[self.final_pos] = ord("z")

    @staticmethod
    def calculate_manhattan_distance(curr_position: Position, goal_position: Position) -> int:
        """given a start and end position calculate the respective Manhattan distance"""
        return int(np.ceil(abs(curr_position[0] - goal_position[0]) + abs(curr_position[1] - goal_position[1])))

    def find_shortest_path(self) -> List[Position]:
        """
        Algorithm https://en.wikipedia.org/wiki/A*_search_algorithm
        given the current object use a-star algorithm to find the shortest path from start to final
        """

        def expand_node(current_node: Position, open_list: Set[Position], closed_list: Set[Position]):
            """
            expand the given node as part of A* Algorithm
            in place modification of open list
            add successor if they are better than the current open list and node is not in closed_list
            """
            # noinspection PyTypeChecker
            successors: List[Position] = [
                tuple_add_tuple(current_node, (1, 0)),
                tuple_add_tuple(current_node, (-1, 0)),
                tuple_add_tuple(current_node, (0, 1)),
                tuple_add_tuple(current_node, (0, -1)),
            ]

            for successor in successors:
                # skip successor on closed list
                if successor in closed_list:
                    continue
                # skip if out of bounds
                if any(axis < 0 for axis in successor) or successor[0] >= self.height or successor[1] >= self.width:
                    continue
                # skip if height difference > 1 -> no step possible
                if self.height_map[successor] - self.height_map[current_node] > 1:
                    continue

                # successor is a valid node, analyse it
                # costs to get to successor is cost to get to current plus one step:
                tentative_g = self.g_value_map[current_node] + 1
                # skip successor if in open list and successor not better than previously
                if successor in open_list and tentative_g >= self.g_value_map[successor]:
                    continue
                # successor is the best current successor
                # update successor minimal g value
                self.g_value_map[successor] = tentative_g
                # update successor link from previous
                self.predecessor_map[successor] = current_node
                # add successor to open list
                h_successor = self.calculate_manhattan_distance(successor, self.final_pos)
                # early skip if f_value is >= self.skip_at
                if tentative_g + h_successor >= self.skip_at:
                    continue
                self.f_value_map[successor] = tentative_g + h_successor
                open_list.add(successor)

        # set open and closed list initial values, and set some type hints
        open_list: Set[Position] = {self.start_pos}
        closed_list: Set[Position] = {self.start_pos}
        self.g_value_map[self.start_pos] = 0  # value to get to start (actually does not matter)
        self.f_value_map[self.start_pos] = 0  # value to get to start (actually does not matter)
        current_node: Position
        curr_node_value: int
        # run algorithm as long as there are values in open list,
        # exits either if a solution is found or when there is no solution
        while len(open_list) != 0:
            # get node from open_list with minimal f value
            current_node: Position = tuple()
            best_value: int = np.inf
            for position in open_list:
                pos_value = self.f_value_map[position]
                if pos_value < best_value:
                    current_node = position
                    best_value = pos_value
            assert best_value != np.inf
            assert current_node != tuple()
            # remove item from open list
            open_list.remove(current_node)

            # if goal reached
            if current_node == self.final_pos:
                # create path from self.successor_map
                path: List[Position] = [self.final_pos]
                prev_node = None
                while prev_node != self.start_pos:
                    prev_node = self.predecessor_map[path[-1]]
                    assert prev_node not in path  # dummy check for infinite loops
                    path.append(prev_node)
                path.reverse()
                return path  # seemingly the start node does not count in the examples

            # ignore current node in subsequent paths, current path is the fastest to curr_node
            closed_list.add(current_node)
            # add all possible next nodes to open_list with respective values
            # modifies open_list in place
            expand_node(current_node, open_list, closed_list)
        return []


def scenic_route_finder(height_map: np.ndarray) -> List[Position]:
    """starting at any square with elevation 'a', find the shortest path to the goal, return path"""
    # set up best path as default path
    default_pathfinder_object = PathFinder(deepcopy(height_map))
    best_path = default_pathfinder_object.find_shortest_path()
    best_g_value_map = deepcopy(default_pathfinder_object.g_value_map)

    # replace default starting position in height_map with "a"
    default_start_pos: Position = tuple(int(x) for x in np.where(height_map == ord("S")))
    height_map[default_start_pos] = ord("a")
    # for every a check shortest path
    for new_start in np.argwhere(height_map == ord("a")):
        new_start = tuple(new_start)
        # skip already analyzed
        if new_start == default_pathfinder_object.start_pos:
            continue

        new_hm = deepcopy(height_map)
        new_hm[new_start] = ord("S")
        new_pathfinder = PathFinder(height_map=new_hm, skip_at=len(best_path), g_value_init=best_g_value_map)
        new_path = new_pathfinder.find_shortest_path()
        if len(new_path) and len(new_path) < len(best_path):
            best_path = new_path
            # speed up successor runs by providing the currently optimal g value map
            best_g_value_map = np.minimum(new_pathfinder.g_value_map, best_g_value_map)
    return best_path


class Test2022Day12(unittest.TestCase):
    test_height_map = np.array(read_lines_as_list(filepath="data/12-test.txt", instance_type=ord, split="every"))
    test_path_finder_object = PathFinder(deepcopy(test_height_map))

    # ! careful ! number of steps is len(path) -1 !

    def test_find_length_of_shortest_path_from_start(self):
        self.assertEqual(len(deepcopy(self.test_path_finder_object).find_shortest_path()) - 1, 31)

    def test_find_shortest_path_from_a(self):
        self.assertEqual(len(scenic_route_finder(self.test_height_map)) - 1, 29)


if __name__ == '__main__':
    print(">>> Start Main 12:")
    puzzle_input = np.array(read_lines_as_list(filepath="data/12.txt", instance_type=ord, split="every"))
    print("Part 1): ", len(PathFinder(deepcopy(puzzle_input)).find_shortest_path()) - 1)
    print("Part 2): ", len(scenic_route_finder(deepcopy(puzzle_input))) - 1)
    print("End Main 12<<<")
