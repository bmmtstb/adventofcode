import unittest

from helper.file import load_file_and_split
from helper.tuple import tuple_add_tuple

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
Position = tuple[int, int]
Positions = set[Position]


def load_data(fp: str) -> tuple[Position, Positions, Position]:
    """Get the position of the guard and all the obstacles.
    Additionally, return the size of the grid as (height, width).
    """
    lines = load_file_and_split(fp)
    obstacles: Positions = set()
    guard: Position = None

    for row_idx, row in enumerate(lines):
        for col_idx, val in enumerate(row):
            if val == "#":
                obstacles.add((row_idx, col_idx))
            elif val == "^":
                guard = (row_idx, col_idx)
    assert guard is not None

    return guard, obstacles, (len(lines), len(lines[0]))


def move(guard: Position, obstacles: Positions, shape: Position) -> Positions:
    """Play the game by moving the guard.
    If he bumps into an obstacle, he will change its direction looping through all DIRECTIONS.
    """
    direction_idx = 0
    h, w = shape

    visited = set()
    visited.add(guard)
    new_pos = None

    # while the guard is within the grid
    while 0 <= guard[0] < h and 0 <= guard[1] < w:
        new_pos = tuple_add_tuple(guard, DIRECTIONS[direction_idx])
        if new_pos in obstacles:
            direction_idx = (direction_idx + 1) % 4
            continue
        visited.add(new_pos)
        guard = new_pos

    assert new_pos is not None
    visited.discard(new_pos)

    return visited


def has_loop(guard: Position, obstacles: Positions, shape: Position) -> bool:
    """Play the game by moving the guard.
    If he bumps into an obstacle, he will change its direction looping through all DIRECTIONS.
    Check whether there are any loops in the visited positions by saving position with the respective direction.
    """
    direction_idx = 0
    h, w = shape

    visited = set()
    visited.add((guard, DIRECTIONS[direction_idx]))
    new_pos = None

    # while the guard is within the grid
    while 0 <= guard[0] < h and 0 <= guard[1] < w:
        new_pos = tuple_add_tuple(guard, DIRECTIONS[direction_idx])
        if new_pos in obstacles:
            direction_idx = (direction_idx + 1) % 4
            continue
        # skip if the new position with the current direction is already visited
        if (new_pos, DIRECTIONS[direction_idx]) in visited:
            return True
        visited.add((new_pos, DIRECTIONS[direction_idx]))
        guard = new_pos
    return False


def visualize(obstacles: Positions, visited: Positions, shape: Position) -> str:
    """Visualize the visited positions."""
    h, w = shape
    grid = [["." for _ in range(w)] for _ in range(h)]

    for r_i, c_i in obstacles:
        assert grid[r_i][c_i] == "."
        grid[r_i][c_i] = "#"

    for r_i, c_i in list(visited):
        assert 0 <= r_i < h and 0 <= c_i < w, f"Out of bounds: {r_i, c_i}"
        assert grid[r_i][c_i] == "."
        grid[r_i][c_i] = "X"

    return "\n".join(["".join(row) for row in grid])


def part1(guard: Position, obstacles: Positions, shape: Position) -> Positions:
    """Part1: Let the guard move. Return the number of unique visited positions."""
    visited = move(guard, obstacles, shape)

    return visited


def part2(
    guard: Position, obstacles: Positions, shape: Position, visited: Positions
) -> int:
    """Part2: For every visited position, place a new obstacle and check whether a loop was created."""
    loop_count = 0
    for pos in visited:
        obstacles.add(pos)
        if has_loop(guard, obstacles, shape):
            loop_count += 1
        obstacles.discard(pos)

    return loop_count


class Test2024Day06(unittest.TestCase):

    fp = "./data/06-test.txt"
    test_data = load_data(fp)

    def test_load_data(self):
        guard, obstacles, size = self.test_data
        self.assertEqual(len(obstacles), 8)
        self.assertEqual(guard, (6, 4))
        self.assertEqual(size, (10, 10))

    def test_p1(self):
        guard, obstacles, size = self.test_data
        self.assertEqual(len(part1(guard, obstacles, size)), 41)

    def test_p2(self):
        guard, obstacles, size = self.test_data
        visited = part1(guard, obstacles, size)
        self.assertEqual(part2(guard, obstacles, size, visited), 6)


if __name__ == "__main__":
    print(">>> Start Main 06:")
    puzzle_guard, puzzle_obs, puzzle_shape = load_data("./data/06.txt")
    sol_p1 = part1(puzzle_guard, puzzle_obs, puzzle_shape)
    print("Part 1): ", len(sol_p1))
    print("Part 2): ", part2(puzzle_guard, puzzle_obs, puzzle_shape, sol_p1))
    print("End Main 06<<<")
