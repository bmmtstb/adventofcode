import unittest
from copy import deepcopy

from typing import Dict, List, Tuple

# s pos
# e pos
from helper.tuple import tuple_add_tuple
from helper.file import read_lines_as_list

directions = {
    "e": (1, 0),
    "w": (-1, 0),
    "se": (0.5, 1),
    "sw": (-0.5, 1),
    "ne": (0.5, -1),
    "nw": (-0.5, -1),
}


def follow_direction(dirs: str) -> Tuple[int, int]:
    """follow a string of given instructions and change the tile at the end"""
    pos = (0, 0)
    i = 0
    while i < len(dirs):
        # change position
        if dirs[i] == "e" or dirs[i] == "w":
            pos = tuple_add_tuple(pos, directions[dirs[i]])
            i += 1
        else:
            pos = tuple_add_tuple(pos, directions[dirs[i : i + 2]])
            i += 2
    return pos


def follow_directions(dirs: List[str]) -> Dict[Tuple[int, int], bool]:
    """follow a set of instructions"""
    colored_tiles = {}
    for dir in dirs:
        tile = follow_direction(dir)
        if tile in colored_tiles:
            colored_tiles[tile] = not colored_tiles[tile]
        else:
            colored_tiles[tile] = True
    return colored_tiles


def count_active(tiles: Dict[Tuple[int, int], bool]) -> int:
    """count active tiles"""
    return sum(1 if tile else 0 for tile in tiles.values())


def get_adjacent_tile_colors(
    colored: Dict[Tuple[int, int], bool], tile: Tuple[int, int]
) -> Dict[bool, int]:
    """get the colors of all adjacent tiles"""
    adjacent = {False: 0, True: 0}
    for curr_dir in directions.values():
        new = tuple_add_tuple(curr_dir, tile)
        if new in colored:
            adjacent[colored[new]] += 1
        else:
            adjacent[False] += 1
    return adjacent


def tile_colors_after_n_days(
    colored: Dict[Tuple[int, int], bool], n: int = 100
) -> Dict[Tuple[int, int], bool]:
    """get the number of active tiles after n days"""
    for _ in range(n):
        # work on duplicate of data
        new_colored = deepcopy(colored)
        # add neighboring tiles
        for tile in colored.keys():
            for curr_dir in directions.values():
                new = tuple_add_tuple(curr_dir, tile)
                if not new in new_colored:
                    new_colored[new] = False
        # for every tile check adjacent tiles and calculate changes
        for tile in new_colored.keys():
            adjacent = get_adjacent_tile_colors(colored, tile)
            if new_colored[tile] and (0 == adjacent[True] or adjacent[True] > 2):
                new_colored[tile] = False
            elif not new_colored[tile] and adjacent[True] == 2:
                new_colored[tile] = True
        colored = new_colored
    return colored


class Test2020Day24(unittest.TestCase):
    test_dirs = [
        "sesenwnenenewseeswwswswwnenewsewsw",
        "neeenesenwnwwswnenewnwwsewnenwseswesw",
        "seswneswswsenwwnwse",
        "nwnwneseeswswnenewneswwnewseswneseene",
        "swweswneswnenwsewnwneneseenw",
        "eesenwseswswnenwswnwnwsewwnwsene",
        "sewnenenenesenwsewnenwwwse",
        "wenwwweseeeweswwwnwwe",
        "wsweesenenewnwwnwsenewsenwwsesesenwne",
        "neeswseenwwswnwswswnw",
        "nenwswwsewswnenenewsenwsenwnesesenew",
        "enewnwewneswsewnwswenweswnenwsenwsw",
        "sweneswneswneneenwnewenewwneswswnese",
        "swwesenesewenwneswnwwneseswwne",
        "enesenwswwswneneswsenwnewswseenwsese",
        "wnwnesenesenenwwnenwsewesewsesesew",
        "nenewswnwewswnenesenwnesewesw",
        "eneswnwswnwsenenwnwnwwseeswneewsenese",
        "neswnwewnwnwseenwseesewsenwsweewe",
        "wseweeenwnesenwwwswnew",
    ]
    colors = follow_directions(deepcopy(test_dirs))

    def test_changed_tiles(self):
        for direction, res in [["esew", {(0.5, 1): True}], ["nwwswee", {(0, 0): True}]]:
            with self.subTest():
                self.assertEqual(follow_directions([direction]), res)

    def test_count(self):
        dirs = follow_directions(deepcopy(self.test_dirs))
        self.assertEqual(count_active(dirs), 10)

    def test_after_n_days(self):
        for n, count in [
            [1, 15],
            [2, 12],
            [5, 23],
            [10, 37],
            [100, 2208],
        ]:
            with self.subTest():
                colors = tile_colors_after_n_days(deepcopy(self.colors), n)
                self.assertEqual(count_active(colors), count)


if __name__ == "__main__":
    print(">>> Start Main 24:")
    puzzle_input = read_lines_as_list("data/24.txt")
    print("Part 1):")
    puzzle_dirs = follow_directions(deepcopy(puzzle_input))
    print(count_active(puzzle_dirs))
    print("Part 2):")
    puzzle_colors = tile_colors_after_n_days(deepcopy(puzzle_dirs))
    print(count_active(puzzle_colors))
    print("End Main 24<<<")
