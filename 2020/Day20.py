import unittest
from copy import deepcopy

from parameterized import parameterized
from typing import Dict, List, Tuple, Set

from tuple_helper import tuple_add_tuple

sea_monster = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   "
]


def load_tiles_from_file(filepath: str) -> Dict[int, List[str]]:
    """load equations from file"""
    with open(filepath) as file:
        raw_tiles = file.read().split("\n\n")
    tiles = {}
    for tile in raw_tiles:
        title, *content = tile.split("\n")
        id = int(title[:-1].split(" ")[1])  # remove : and split at " " to get number
        tiles[id] = content
    return tiles


def get_tile_sides(tile_content: List[str]) -> Tuple[str, str, str, str]:
    """calculate the sides of a tile -> returns values of 0 Top, 1 Right, 2 Bottom, 3 Left side"""
    top = tile_content[0]  # left to right
    bottom = tile_content[-1]  # left to right
    left = "".join(row[0] for row in tile_content)  # top to bottom
    right = "".join(row[-1] for row in tile_content)  # top to bottom
    return top, right, bottom, left


def find_matching_tiles(tiles: Dict[int, Tuple[str, str, str, str]], curr_tile: Tuple[str, str, str, str],
                        curr_tile_id: int) -> List[Tuple[int, int, int]]:
    """
    Find all the matching tiles for a single tile
    returns tile id, curr tile side and found side, the value is negative if the side is reversed
    """
    matches = []
    # get ids of all matching ids
    for tile_key, tile_val in tiles.items():
        # add id as long as its not the same item
        if curr_tile_id != tile_key:
            for i, side in enumerate(tile_val):
                if side in curr_tile:
                    matches.append((tile_key, curr_tile.index(side), i))
                if side[::-1] in curr_tile:  # may be reversed
                    # -4 == "-0"
                    matches.append((tile_key, curr_tile.index(side[::-1]), -i if i != 0 else -4))
    return matches


def rotate_tile(op: str, tile: List[str]):
    """
    rotate or mirror the given tile
    values for operation
    h: left becomes right
    v: top becomes bottom
    r180: rotate 180° (same as h+v)
    r90: rotate 90° clockwise
    r270: rotate 270° clockwise
    """
    data = deepcopy(tile)
    if op == "r180" or op == "v":
        data = data[::-1]
    if op == "r180" or op == "h":
        data = [d[::-1] for d in data]
    if op == "r90":
        data = ["".join(data[len(data) - 1 - j][i] for j in range(len(data))) for i in range(len(data[0]))]
    elif op == "r270":
        data = ["".join(data[j][len(data[0]) - 1 - i] for j in range(len(data))) for i in range(len(data[0]))]
    return data



def get_puzzle_sides(tiles: Dict[int, List[str]]) -> Dict[int, Tuple[str, str, str, str]]:
    """for every tile get the matching tiles"""
    tile_sides = {}
    for tile_key, tile_val in tiles.items():
        tile_sides[tile_key] = tuple(get_tile_sides(tile_val))
    return tile_sides


def get_puzzle_matching(tile_sides: Dict[int, Tuple[str, str, str, str]]) -> Dict[int, List[Tuple[int, int, int]]]:
    """get the matching tiles for every tile"""
    matching_ids = {}
    for tile_id, tile in tile_sides.items():
        matching_ids[tile_id] = find_matching_tiles(tile_sides, tile, tile_id)
    return matching_ids


def get_puzzle_corners(tiles: Dict[int, List[str]]) -> int:
    """Solve the puzzle by getting all the matching puzzle pieces until nothing is matching"""
    # get a dict of all the tile sides
    tile_sides = get_puzzle_sides(tiles)
    # find matching tiles for every tile
    matching_ids = get_puzzle_matching(tile_sides)

    # corner tile iff only 2 matching
    corner_val = 1
    for key, val in matching_ids.items():
        if len(val) == 2:
            corner_val *= key
    return corner_val


def get_key_from_val(my_dict: Dict[int, Tuple[int, int]], val: Tuple[int, int]):
    """get specific key from dictionary"""
    for key, value in my_dict.items():
        if val == value:
            return key
    raise Exception("key doesn't exist")


# Turn helper
# Old   | New   | Diff  | turn | keeps_dir
#  0      1        -1      90       -
#  0      3        -3      270      +
#  1      0         1      270      -
#  1      2        -1      90       +
#  2      1         1      270      +
#  3      3        -1      90       -
#  4      0         3      90       +
#  4      2         1      270      -
def assemble_puzzle(tiles: Dict[int, List[str]]) -> List[str]:
    """get the final puzzle image"""
    # get a dict of all the tile sides
    tile_sides = get_puzzle_sides(tiles)
    # find matching tiles for every tile
    matching_ids = get_puzzle_matching(tile_sides)
    # start from one tile and add all matching ids to the current stack
    curr_key, stack = list(matching_ids.items())[0]
    tile_height = len(tiles[curr_key])
    stack = list([(curr_key, *item)[:4] for item in stack])
    stack: List[Tuple[int, int, int, int]]
    # init first tile position to (0,0) (-> numbers may be negative if its the wrong corner!)
    positions: Dict[int, Tuple[int, int]]
    positions = {curr_key: (0, 0)}
    while len(stack) > 0:
        # take one new item from stack
        old_tile_id, new_tile_id, old_side_pos, new_side_pos = stack[0]
        new_tile = tiles[new_tile_id]
        old_pos = positions[old_tile_id]

        # rotate the tile according to reference tile
        if old_side_pos < 0:
            raise Exception("old id is negative")
        if (old_side_pos + new_side_pos) % 2 != 0:  # rotation by 90° or 270°
            diff = (abs(old_side_pos) - abs(new_side_pos)) % 4
            if diff == -1 or diff == 3:  # 90°
                new_tile = rotate_tile("r90", new_tile)
            else:  # 270°
                new_tile = rotate_tile("r270", new_tile)
            # Special cases -> change direction to keep orientation of sides consistent
            # case positive
            if old_side_pos == 0 and new_side_pos == 1:
                new_tile = rotate_tile("h", new_tile)
            elif old_side_pos == 1 and new_side_pos == 0:
                new_tile = rotate_tile("v", new_tile)
            elif old_side_pos == 2 and new_side_pos == 3:
                new_tile = rotate_tile("h", new_tile)
            elif old_side_pos == 3 and new_side_pos == 2:
                new_tile = rotate_tile("v", new_tile)
            # case negative
            elif old_side_pos == 0 and new_side_pos == -3:
                new_tile = rotate_tile("h", new_tile)
            elif old_side_pos == 1 and new_side_pos == -2:
                new_tile = rotate_tile("v", new_tile)
            elif old_side_pos == 2 and new_side_pos == -1:
                new_tile = rotate_tile("h", new_tile)
            elif old_side_pos == 3 and new_side_pos == -4:
                new_tile = rotate_tile("v", new_tile)

        elif abs(new_side_pos) % 2 != 0:  # abs = 1, 3 -> match left and right sides
            if old_side_pos == abs(new_side_pos):  # rotate left to right
                new_tile = rotate_tile("h", new_tile)
            if new_side_pos < 0:  # mirror left to right to invert top and bottom sides
                new_tile = rotate_tile("v", new_tile)

        else:  # abs = 0, 2, 4 -> match top and bottom sides
            if old_side_pos == abs(new_side_pos) % 4:  # rotate top to bottom
                new_tile = rotate_tile("v", new_tile)
            if new_side_pos < 0:  # mirror top to bottom to invert left and right sides
                new_tile = rotate_tile("h", new_tile)

        # save tile and tile position
        tiles[new_tile_id] = deepcopy(new_tile)
        diff_pos = (
            1 if abs(old_side_pos) == 1 else -1 if abs(old_side_pos) == 3 else 0,
            -1 if abs(old_side_pos) % 4 == 0 else 1 if abs(old_side_pos) == 2 else 0
        )
        #  int id: pos (x,y)
        positions[new_tile_id] = tuple_add_tuple(old_pos, diff_pos)
        # get new tile sides and change orientation of neighbors
        new_tile_sides = get_tile_sides(new_tile)
        tile_sides[new_tile_id] = new_tile_sides
        matching = find_matching_tiles(tile_sides, new_tile_sides, new_tile_id)
        # modify current stack: remove all items that refer to curr item
        stack = [stack_item for stack_item in stack if stack_item[1] != new_tile_id]
        # modify future stack: add new edges that are not on stack
        for item in matching:
            if not (item[0]) in positions.keys():  # skip tiles that have been added yet
                stack.append((new_tile_id, *item)[:4])
    # get top left item (min vals)
    min_x = min(pos[0] for pos in positions.values())
    min_y = min(pos[1] for pos in positions.values())
    max_x = max(pos[0] for pos in positions.values())
    max_y = max(pos[1] for pos in positions.values())
    # put every puzzle piece in its place
    arranged_pieces: List[list] = [[None for __ in range(abs(max_x - min_x + 1))] for _ in range(abs(max_y - min_y + 1))]
    for pos_id, pos in positions.items():
        tile_content = tiles[pos_id]  # don't know why, but I need to invert all the pieces top to bottom once
        tile_content_cut = tile_content[1:-1]
        tile_content_cut = [line[1:-1] for line in tile_content_cut]
        arranged_pieces[pos[1] - min_y][pos[0] - min_x] = tile_content
        # arranged_pieces[pos[1] - min_y][pos[0] - min_x] = tile_content_cut
    # puzzle is assembled -> remove edges from every tile and assemble it to one big list of strings
    height_wo_borders = tile_height - 2
    assembled = ["" for _ in range(abs(max_y - min_y + 1) * height_wo_borders)]  # init to correct length
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            pos = (x, y)
            tile_id = get_key_from_val(positions, pos)
            tile_content = tiles[tile_id]  # don't know why, but I need to invert all the pieces top to bottom once
            tile_content_cut = tile_content[1:-1]
            tile_content_cut = [line[1:-1] for line in tile_content_cut]
            for i in range(len(tile_content_cut)):
                y_offset = y - min_y
                assembled[i + height_wo_borders * y_offset] += tile_content_cut[i]
    return assembled


def search_seamonsters(puzzle: List[str]) -> int:
    """get the number of sea monsters in the puzzle"""
    count = 0
    monster_width = len(sea_monster)
    monster_height = len(sea_monster[0])
    for puzzle_i in range(0, len(puzzle) - monster_width):
        for puzzle_j in range(0, len(puzzle[puzzle_i]) - monster_height):
            # check if a sea monster starts here
            if all(puzzle[puzzle_i + sm_i][puzzle_j + sm_j] == "#"
                    for sm_j in range(len(sea_monster[0]))
                        for sm_i in range(len(sea_monster))
                            if sea_monster[sm_i][sm_j] == "#"
                   ):
                count += 1
    return count


def get_max_seamonsters(puzzle: List[str]) -> int:
    """get the number of sea monsters for every possible rotation and mirroring of the complete puzzle"""
    p = deepcopy(puzzle)
    max_monsters = 0
    for h_mirr in range(2):
        p = rotate_tile("h", p)
        for v_mirr in range(2):
            p = rotate_tile("v", p)
            for rot in range(4):
                p = rotate_tile("r90", p)
                monsters = search_seamonsters(p)
                max_monsters = max(monsters, max_monsters)
    return max_monsters


def get_roughness(puzzle: List[str]) -> int:
    """get the water roughness"""
    roughness = sum(sum(1 if c == "#" else 0 for c in line) for line in puzzle)
    sea_monster_tiles = sum(sum(1 if c == "#" else 0 for c in line) for line in sea_monster)

    sea_monster_count = get_max_seamonsters(puzzle)
    return roughness - sea_monster_tiles * sea_monster_count


class Test2020Day20(unittest.TestCase):
    test_tiles = load_tiles_from_file("data/20-test.txt")
    complete = [".#.#..#.##...#.##..#####", "###....#.#....#..#......", "##.##.###.#.#..######...",
                "###.#####...#.#####.#..#", "##.#....#.##.####...#.##", "...########.#....#####.#",
                "....#..#...##..#.#.###..", ".####...#..#.....#......", "#..#.##..#..###.#.##....",
                "#.####..#.####.#.#.###..", "###.#.#...#.######.#..##", "#.####....##..########.#",
                "##..##.#...#...#.#.#.#..", "...#..#..#.#.##..###.###", ".#.#....#.##.#...###.##.",
                "###.#...#..#.##.######..", ".#.#.###.##.##.#..#.##..", ".####.###.#...###.#..#.#",
                "..#.#..#..#.#.#.####.###", "#..####...#.#.#.###.###.", "#####..#####...###....##",
                "#.##..#..#...#..####...#", ".#.###..##..##..####.##.", "...###...##...#...#..###"]
    # tile = ["..##.#..#.", "##..#.....", "#...##..#.", "####.#...#", "##.##.###.", "##...#.###", ".#.#.#..##",
    #         "..#....#..", "###...#.#.", "..###..###"]
    tile = test_tiles[2311]

    def test_get_sides(self):
        self.assertEqual(get_tile_sides(self.tile), ("..##.#..#.", "...#.##..#", "..###..###", ".#####..#."))

    def test_puzzle_corners(self):
        self.assertEqual(get_puzzle_corners(self.test_tiles), 20899048083289)

    def test_rotation_90(self):
        tile = deepcopy(self.tile)
        ninty = rotate_tile("r90", tile)
        threesixty = rotate_tile("r270", ninty)
        self.assertListEqual(threesixty, tile)
        ninty = rotate_tile("r90", ninty)
        ninty = rotate_tile("r90", ninty)
        self.assertListEqual(rotate_tile("r270", tile), ninty)

    def test_rotation_180(self):
        tile = deepcopy(self.tile)
        oneeighty = rotate_tile("r180", tile)
        threesixty = rotate_tile("r180", oneeighty)
        ninty = rotate_tile("r90", tile)
        twice_ninty = rotate_tile("r90", ninty)
        self.assertListEqual(self.tile, threesixty)
        self.assertListEqual(oneeighty, twice_ninty)

    def test_count_seamonsters(self):
        self.assertEqual(get_max_seamonsters(self.complete), 2)

    def test_roughness(self):
        self.assertEqual(get_roughness(self.complete), 273)

    def test_complete_puzzle(self):
        self.assertListEqual(assemble_puzzle(self.test_tiles), rotate_tile("v", self.complete))


if __name__ == '__main__':
    print(">>> Start Main 20:")
    puzzle_input = load_tiles_from_file("data/20.txt")
    print("Part 1):")
    print(get_puzzle_corners(deepcopy(puzzle_input)))
    print("Part 2):")
    print(get_roughness(assemble_puzzle(deepcopy(puzzle_input))))
    # not
    # 2095 too high
    print("End Main 20<<<")
