import unittest
from copy import deepcopy

from typing import Dict, List, Tuple, Set

from helper.tuple import tuple_add_tuple, tuple_mod_number, tuple_mult_scalar


def play_deterministic_dirac(starting_pos: List[int]) -> (int, int):
    """play a game until score 1000 is reached, return number of dice rolled and losing score summed"""
    winning_score: int = 1000
    dice_size: int = 100
    throw_amount: int = 3
    board_size: int = 10
    # init
    dice = list(range(1, dice_size + 1)) + list(range(1, throw_amount + 1))
    nof_players = len(starting_pos)
    nof_dice_rolled = 0
    scores = [0] * nof_players
    curr_pos = [pos - 1 for pos in starting_pos]  # zero-indexed
    player_turn = 0

    # play the game
    while not any(score >= winning_score for score in scores):
        # roll dice
        dice_sum = sum(dice[(nof_dice_rolled % dice_size):(nof_dice_rolled % dice_size + throw_amount)])
        # increase rolls
        nof_dice_rolled += throw_amount
        # move player
        curr_pos[player_turn] = (curr_pos[player_turn] + dice_sum) % board_size
        # add score
        scores[player_turn] += curr_pos[player_turn] + 1  # +1 due to zero-indexed
        # switch turn
        player_turn = (player_turn + 1) % nof_players

    # the winner is:
    return nof_dice_rolled, sum(score if score < winning_score else 0 for score in scores)


def play_quantum_dirac(starting_pos: List[int]) -> int:
    """find the player that wins in more universes using the quantum die, return the amount"""
    dice_sum_possibilities = {  # sum of three scores -> number of times this occurs
        3: 1,
        4: 3,
        5: 6,
        6: 7,
        7: 6,
        8: 3,
        9: 1,
    }
    player_wins = [0, 0]
    player_turn = 0

    curr_scores: Dict[Tuple[int], Dict[Tuple[int, int], int]] = {
        tuple(pos - 1 for pos in starting_pos): {(0, 0): 1}  # again zero-indexed positions
    }
    while len(curr_scores.keys()):
        new_scores: Dict[Tuple[int], Dict[Tuple[int, int], int]] = dict()
        curr_base: Tuple[int, int] = (0, 1) if player_turn else (1, 0)

        # given current player, add possible dice combination to every poss score
        for dice_sum, nof_times in dice_sum_possibilities.items():
            for pos, old_scores in curr_scores.items():
                # move curr player forward
                new_pos = tuple_mod_number(tuple_add_tuple(tuple_mult_scalar(curr_base, dice_sum), pos), 10)
                # update all scores
                for old_score, old_count in old_scores.items():
                    # add new position to score(s)
                    new_score: Tuple[int, int] = tuple_add_tuple(old_score, tuple_mult_scalar(curr_base, new_pos[player_turn] + 1))
                    # the current sum may be rolled multiple times
                    new_count = nof_times * old_count
                    # check if player won
                    if new_score[player_turn] >= 21:
                        player_wins[player_turn] += new_count
                    # otherwise, add new board state to possibilities
                    else:
                        if new_pos not in new_scores:
                            new_scores[new_pos] = dict()
                        # increase count of that state-score pair
                        if new_score in new_scores[new_pos]:
                            new_scores[new_pos][new_score] += new_count
                        else:
                            new_scores[new_pos][new_score] = new_count
        # update scores
        curr_scores = deepcopy(new_scores)
        player_turn = 0 if player_turn else 1
    return max(player_wins)


class Test2021Day21(unittest.TestCase):
    def test_play_deterministic_game(self):
        throws, loosing = play_deterministic_dirac([4, 8])
        self.assertEqual(throws, 993)
        self.assertEqual(loosing, 745)

    def test_play_quantum_game(self):
        max_wins = play_quantum_dirac([4, 8])
        self.assertEqual(max_wins, 444356092776315)


if __name__ == '__main__':
    print(">>> Start Main 21:")
    puzzle_input = "Player 1 starting position: 3" \
                   "Player 2 starting position: 5"
    throws, loosing = play_deterministic_dirac([3, 5])
    print("Part 1): ", throws * loosing)
    print("Part 2): ", play_quantum_dirac([3, 5]))
    print("End Main 21<<<")
