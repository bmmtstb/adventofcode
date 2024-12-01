import unittest
from copy import deepcopy
from typing import Dict, List, Tuple, Set

from helper.file import read_lines_as_list

# A for Rock
# B for Paper
# C for Scissors

# p1
# X for Rock -> 1
# Y for Paper -> 2
# Z for Scissors -> 3
shape_scores = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}

Match = Tuple[str, str]
Guide = List[Match]


def load_strategy_guide(filepath: str) -> Guide:
    """load the strategy guide from file"""
    return read_lines_as_list(filepath=filepath, split=" ", instance_type=str)


def get_match_score(m: Match) -> int:
    """get the score of one individual match"""
    # outcome_score = loose: 0, draw: 3, win: 6
    # total score = sum(scores per round)
    # score per round = shape_score + outcome_score
    if ord(m[1]) - ord(m[0]) == 23:
        outcome_score = 3
    elif (ord(m[1]) - ord(m[0])) % 3 == 0:
        outcome_score = 6
    else:
        outcome_score = 0
    return shape_scores[m[1]] + outcome_score


def get_strategy_guide_score(guide: Guide) -> int:
    """get the total score of the correct strategy guide"""
    return sum(get_match_score(match) for match in guide)


# p2
# X for loose
# Y for draw
# Z for win
def get_correct_symbol(guide: Guide) -> Guide:
    """replace the right symbol with the one the character is going to play"""
    guide = deepcopy(guide)
    for i, match in enumerate(guide):
        enemy_play, game_result = match
        if game_result == "Y":
            guide[i] = (enemy_play, chr(ord(enemy_play) + 23))
        elif game_result == "X":  # loose
            guide[i] = (
                enemy_play,
                "X" if enemy_play == "B" else "Y" if enemy_play == "C" else "Z",
            )
        else:  # win
            guide[i] = (
                enemy_play,
                "X" if enemy_play == "C" else "Y" if enemy_play == "A" else "Z",
            )
    return guide


class Test2022Day02(unittest.TestCase):
    test_guide: Guide = [("A", "Y"), ("B", "X"), ("C", "Z")]
    test_self_play: Guide = [("A", "X"), ("B", "X"), ("C", "X")]

    def test_get_strategy_guide_score(self):
        self.assertEqual(get_strategy_guide_score(self.test_guide), 15)
        self.assertEqual(get_strategy_guide_score(self.test_self_play), 12)

    def test_get_match_score(self):
        for match_index, score in [
            (0, 8),
            (1, 1),
            (2, 6),
        ]:
            with self.subTest(msg=f"match {match_index} should have score {score}"):
                self.assertEqual(get_match_score(self.test_guide[match_index]), score)

    def test_get_correct_symbol(self):
        self.assertEqual(get_correct_symbol(self.test_guide), self.test_self_play)


if __name__ == "__main__":
    print(">>> Start Main 02:")
    puzzle_input = load_strategy_guide("data/02.txt")

    print("Part 1): ", get_strategy_guide_score(puzzle_input))
    print("Part 2): ", get_strategy_guide_score(get_correct_symbol(puzzle_input)))
    print("End Main 02<<<")
