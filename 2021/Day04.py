import unittest
from typing import Dict, List, Tuple, Set

from helper.file import load_file_and_split


def parse_data(filepath: str) -> (List[int], List[List[int]]):
    """load the random Numbers and boards from the file"""
    parts = load_file_and_split(filepath, "\n\n")
    numbers = [int(num) for num in parts[0].split(",")]
    boards = []
    for board in parts[1:]:
        board_data = []
        for line in board.split("\n"):
            board_data += [int(line[i:i + 3].strip()) for i in range(0, len(line), 3)]
        boards.append(board_data)
    return numbers, boards


def play_bingo(numbers: List[int], boards: List[List[int]]) -> int:
    """play bingo, only horiz and vert lines count - return sum of not-chosen numbers times last digit"""
    for number in numbers:
        for board in boards:
            try:
                # mark the number on every board
                idx: int = board.index(number)
                board[idx] = None
                # check changed boards for lines using idx
                remainder = idx % 5
                row_start = (idx - remainder)
                # horizontal (neighbors) or vertical (every fifth)
                if all(val is None for val in board[row_start:row_start + 5]) or \
                        all(val is None for val in board[remainder::5]):
                    return number * sum(val for val in board if val is not None)

            except ValueError:
                pass
    raise Exception("No valid field found.")


def last_board(numbers: List[int], boards: List[List[int]]) -> int:
    """play every board until every board won at least once, return sum of the last board"""
    for number in numbers:
        remove_ids = []
        for board_id, board in enumerate(boards):
            try:
                # mark the number on every board
                idx: int = board.index(number)
                board[idx] = None
                # check changed boards for lines using idx
                remainder = idx % 5
                row_start = (idx - remainder)
                # horizontal (neighbors) or vertical (every fifth)
                if all(val is None for val in board[row_start:row_start + 5]) or \
                        all(val is None for val in board[remainder::5]):
                    # save id for removal
                    remove_ids.append(board_id)
                    # current board is final board -> worst choice
                    if len(boards) - len(remove_ids) == 0:
                        return number * sum(val for val in board if val is not None)
            except ValueError:
                pass
        # remove boards from possible choices
        boards = [boards[i] for i in range(len(boards)) if i not in remove_ids]
    raise Exception("No valid field found.")



class Test2021Day04(unittest.TestCase):

    def test_basic_bingo(self):
        num, boards = parse_data("data/04-test.txt")
        self.assertEqual(play_bingo(num, boards), 4512)

    def test_last_board(self):
        num, boards = parse_data("data/04-test.txt")
        self.assertEqual(last_board(num, boards), 1924)


if __name__ == '__main__':
    print(">>> Start Main 04:")
    puzzle_input_numbers, puzzle_input_boards = parse_data("data/04.txt")
    print("Part 1): ", play_bingo(puzzle_input_numbers, puzzle_input_boards))
    puzzle_input_numbers, puzzle_input_boards = parse_data("data/04.txt")
    print("Part 2): ", last_board(puzzle_input_numbers, puzzle_input_boards))
    print("End Main 04<<<")
