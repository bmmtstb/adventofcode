import unittest
from parameterized import parameterized
from typing import Dict, List, Tuple, Set
from copy import deepcopy


def load_from_file(filepath: str) -> List[str]:
    """load equations from file"""
    with open(filepath) as file:
        players = file.read().split("\n\n")
    return players


def load_player_cards(players: List[str]) -> List[List[int]]:
    """load the cards of the players"""
    players_cards = []
    for player in players:
        player_cards = []
        for i, number in enumerate(player.split("\n")):
            if i > 0:
                player_cards.append(int(number))
        players_cards.append(player_cards)
    return players_cards


def play_game(piles: List[List[int]]) -> (int, int, List[int]):
    """Play a game of combat, return winner id, nof turns and pile of winner"""
    n = 0
    winner = None
    while not any(len(pile) == 0 for pile in piles):
        round_cards = []
        for pile in piles:
            round_cards.append(pile.pop(0))
        winner = round_cards.index(max(round_cards))
        round_cards.sort(reverse=True)
        piles[winner] = piles[winner] + round_cards
        n += 1
    return winner, n, piles[winner]


def get_deck_score(deck: List[int]) -> int:
    """get the score of a specific deck of cards"""
    deck.reverse()
    return sum((i + 1) * card for i, card in enumerate(deck))


def play_recursive_combat(piles: List[List[int]]) -> (int, List[int]):
    """Play a game of recursive combat, return winner_id and winning pile"""
    if len(piles) != 2:
        raise Exception("more than 2 players not supported")
    history = []
    while not any(len(pile) == 0 for pile in piles):
        # check for same state
        if piles in history:
            return 0, piles[0]
        # keep history up to date
        history.append(deepcopy(piles))
        draw0 = piles[0].pop(0)
        draw1 = piles[1].pop(0)
        if len(piles[0]) >= draw0 and len(piles[1]) >= draw1:  # play recursive combat
            # get new lists
            list0 = deepcopy(piles[0][:draw0])
            list1 = deepcopy(piles[1][:draw1])
            win_id, _ = play_recursive_combat([list0, list1])
            if win_id == 0:
                piles[0].append(draw0)
                piles[0].append(draw1)
            else:
                piles[1].append(draw1)
                piles[1].append(draw0)
        else:  # no recursion possible
            # append cards of last round to state
            if draw0 > draw1:
                piles[0].append(draw0)
                piles[0].append(draw1)
            else:
                piles[1].append(draw1)
                piles[1].append(draw0)
    # get winner and deck
    if len(piles[0]) == 0:
        return 1, piles[1]
    else:
        return 0, piles[0]


class Test2020Day22(unittest.TestCase):
    test_string = ["Player 1:\n9\n2\n6\n3\n1", "Player 2:\n5\n8\n4\n7\n10"]
    players_cards = load_player_cards(test_string)

    def test_game_v1_state(self):
        id, n, pile = play_game(deepcopy(self.players_cards))
        self.assertEqual(id, 1)
        self.assertEqual(n, 29)
        self.assertEqual(get_deck_score(pile), 306)

    def test_game_v2_state(self):
        id, pile = play_recursive_combat(deepcopy(self.players_cards))
        self.assertEqual(id, 1)
        self.assertListEqual(pile, [7, 5, 6, 2, 4, 1, 10, 8, 9, 3])
        self.assertEqual(get_deck_score(pile), 291)


if __name__ == '__main__':
    print(">>> Start Main 22:")
    puzzle_input_str = load_from_file("data/22.txt")
    puzzle_input = load_player_cards(puzzle_input_str)
    print("Part 1):")
    win_id, n, pile = play_game(deepcopy(puzzle_input))
    print(get_deck_score(pile))
    print("Part 2):")
    _, pile = play_recursive_combat(deepcopy(puzzle_input))
    print(get_deck_score(pile))
    print("End Main 22<<<")
