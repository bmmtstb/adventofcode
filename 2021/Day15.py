import unittest
from copy import deepcopy
from typing import Dict, List, Tuple, Set

from helper.file import read_lines_as_list

Cost = int
Map = List[List[int]]
Node = Tuple[int, int, Cost]  # x, y, val
Path = List[Node]


def risk_of_path(p: Path) -> Cost:
    """calculate the risk of a given path"""
    return sum(node[2] for node in p[1:])


def repeat_risk_map(rm: Map) -> Map:
    """given a risk map, repeat it 5 times left and down, while adding 1 to every risk"""
    size_x: int = len(rm[0])
    size_y: int = len(rm)
    # repeat
    rm = [deepcopy(row) + deepcopy(row) + deepcopy(row) + deepcopy(row) + deepcopy(row) for row in rm]
    rm += deepcopy(rm) + deepcopy(rm) + deepcopy(rm) + deepcopy(rm)
    # modify values
    for x in range(0, 5 * size_x):
        x_factor = x // size_x
        for y in range(0, 5 * size_y):
            factor = x_factor + y // size_y
            rm[y][x] = (rm[y][x] + factor) % 9 if rm[y][x] + factor > 9 else rm[y][x] + factor
    return rm


def a_star(risk_map: Map, start: Node, goal: Node) -> Path:
    """Run A-Star algorithm on mapped data"""
    "from: https://en.wikipedia.org/wiki/A*_search_algorithm"
    size_x: int = len(risk_map[0])
    size_y: int = len(risk_map)

    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    open_list: Path = [start]

    # current cheapest path
    came_from: Dict[Node, Node] = dict()

    # highest possible score
    highest = sum(sum(val for val in row) for row in risk_map)

    def get_neighbors(curr: Node) -> Path:
        """given a node, get all adjacent nodes"""
        neighbors = []
        if curr[0] - 1 >= 0:
            neighbors.append((curr[0] - 1, curr[1], int(risk_map[curr[1]][curr[0] - 1])))
        if curr[1] - 1 >= 0:
            neighbors.append((curr[0], curr[1] - 1, int(risk_map[curr[1] - 1][curr[0]])))
        if curr[0] + 1 < size_x:
            neighbors.append((curr[0] + 1, curr[1], int(risk_map[curr[1]][curr[0] + 1])))
        if curr[1] + 1 < size_y:
            neighbors.append((curr[0], curr[1] + 1, int(risk_map[curr[1] + 1][curr[0]])))
        return neighbors

    def heuristic(curr_node: Node) -> Cost:
        """return the heuristic of the current point"""
        "equals the minimum amount of steps to reach goal (assuming goal is in bottom right corner)"
        return goal[0] - curr_node[0] + goal[1] - curr_node[1]

    def reconstruct_path(c: Node) -> Path:
        total_path: Path = [c]
        while not(c[0] == start[0] and c[1] == start[1]):
            c = came_from[c]
            total_path.insert(0, c)
        return total_path

    # For node n, node_lowest_score[n] is the cost of the cheapest path from start to n currently known.
    node_lowest_score: Map = [[highest for x_ in range(size_x)]for y_ in range(size_y)]
    node_lowest_score[start[1]][start[0]] = 0

    # For node n, expected_score[n] = node_lowest_score[n] + h(n). expected_score[n] represents our current best guess as to
    # how short a path from start to finish can be if it goes through n.
    expected_score: Map = [[highest for x_ in range(size_x)]for y_ in range(size_y)]
    node_lowest_score[start[1]][start[0]] = heuristic(start)

    while len(open_list) > 0:
        # make sure open_list has the lowest expected value first, then pick lowest
        open_list.sort(key=lambda x: expected_score[x[1]][x[0]])
        current = open_list.pop(0)
        # # check if new point is goal
        if current[0] == goal[0] and current[1] == goal[1]:
            return reconstruct_path(current)

        for neighbor_node in get_neighbors(current):
            # d(current,neighbor_node) is the weight of the edge from current to neighbor_node
            # cost_through_curr is the distance from start to the neighbor_node through current
            cost_through_curr = node_lowest_score[current[1]][current[0]] + neighbor_node[2]
            if cost_through_curr < node_lowest_score[neighbor_node[1]][neighbor_node[0]]:
                # This path to neighbor_node is better than any previous one. Record it!
                came_from[neighbor_node] = current
                node_lowest_score[neighbor_node[1]][neighbor_node[0]] = cost_through_curr
                expected_score[neighbor_node[1]][neighbor_node[0]] = cost_through_curr + heuristic(neighbor_node)
                if neighbor_node not in open_list:
                    open_list.append(neighbor_node)
    # return reconstruct_path(goal)
    # Open set is empty but goal was never reached
    raise Exception("No Path to goal found.")
    


class Test2021Day15(unittest.TestCase):
    def test_astar_example(self):
        test_field: Map = read_lines_as_list("data/15-test.txt", instance_type=int, split="every")
        start: Node = (0, 0, int(test_field[0][0]))
        goal: Node = (len(test_field[0]) - 1, len(test_field) - 1, int(test_field[-1][-1]))
        final_path = a_star(test_field, start, goal)
        self.assertEqual(risk_of_path(final_path), 40)

    def test_repeat(self):
        test_field: Map = read_lines_as_list("data/15-test.txt", instance_type=int, split="every")
        repeated: Map = read_lines_as_list("data/15-test-repeated.txt", instance_type=int, split="every")
        self.assertListEqual(repeated, repeat_risk_map(test_field))

    def test_astar_repeated_example(self):
        test_field: Map = read_lines_as_list("data/15-test-repeated.txt", instance_type=int, split="every")
        start: Node = (0, 0, int(test_field[0][0]))
        goal: Node = (len(test_field[0]) - 1, len(test_field) - 1, int(test_field[-1][-1]))
        final_path = a_star(test_field, start, goal)
        self.assertEqual(risk_of_path(final_path), 315)


if __name__ == '__main__':
    print(">>> Start Main 15:")
    puzzle_input: Map = read_lines_as_list("data/15.txt", instance_type=int, split="every")
    start: Node = (0, 0, int(puzzle_input[0][0]))
    goal: Node = (len(puzzle_input[0]) - 1, len(puzzle_input) - 1, int(puzzle_input[-1][-1]))
    final_path = a_star(puzzle_input, start, goal)
    print("Part 1): ", risk_of_path(final_path))
    repeated = repeat_risk_map(deepcopy(puzzle_input))
    start: Node = (0, 0, int(repeated[0][0]))
    goal: Node = (len(repeated[0]) - 1, len(repeated) - 1, int(repeated[-1][-1]))
    final_path = a_star(repeated, start, goal)
    print("Part 2): ", risk_of_path(final_path))
    print("End Main 15<<<")
