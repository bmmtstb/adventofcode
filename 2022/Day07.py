import unittest
from typing import Dict, List, Tuple, Set, Union, Iterable

from helper.file import read_lines_as_list

Path = List[str]
FolderStructure = Dict[str, Union[Iterable["FolderStructure"], int]]

TOTAL_FS_SIZE = 70000000
UPDATE_NEEDED_SIZE = 30000000


def get_folder_structure_at_path(folder_structure: FolderStructure, path: Path) -> FolderStructure:
    """
    step into the given folder structure following a given path
    returns the (reference) to the nested object
    """
    curr_item = folder_structure
    for dir_name in path:
        curr_item = curr_item[dir_name]
    return curr_item


def parse_folder_structure(filepath: str) -> FolderStructure:
    """parse the sys log and create the folder structure"""
    # read datastream
    plain_lines: List[List[str]] = read_lines_as_list(filepath=filepath, split=" ")
    # set up loop variables
    current_path: Path = []
    list_directories: bool = False
    full_folder_structure: FolderStructure = {}
    # start loop
    for line in plain_lines:
        # stop list directories
        if line[0] == "$":
            list_directories = False
        # change directory
        if line[0] == "$" and line[1] == "cd":
            if line[2] == "..":  # go back one level
                current_path.pop()
            elif line[2] == "/":  # go to main
                current_path = []
            else:  # go to dir
                current_path.append(line[2])
        # start list directory content
        elif line[0] == "$" and line[1] == "ls":
            list_directories = True
        # read in directories
        elif list_directories:
            # insert new data at current folder level
            structure = get_folder_structure_at_path(full_folder_structure, current_path)
            obj_name = line[1]
            structure[obj_name] = dict() if line[0] == "dir" else int(line[0])
        else:
            raise Exception(f'Unexpected line {line}')
    return full_folder_structure


def get_folder_structure_total_size(folder_structure: FolderStructure) -> int:
    """given a folder structure calculate its total size"""
    sum_of_curr_folder = 0
    for file_object in folder_structure.values():
        if type(file_object) == int:
            # add size of file
            sum_of_curr_folder += file_object
        else:
            # add sum of sub-folder
            sum_of_curr_folder += get_folder_structure_total_size(file_object)
    return sum_of_curr_folder


def find_size_of_small_directories(folder_structure: FolderStructure, max_size: int = 100000) -> int:
    """
    get the total size of all folders that have a size of at most max_size
    returns the accumulated sum of the small directories
    """
    sum_of_curr_folder = 0
    accumulated_sum = 0
    for file_object in folder_structure.values():
        if type(file_object) == int:
            sum_of_curr_folder += file_object
        else:
            # get stats of the nested folder
            sub_accumulated = find_size_of_small_directories(file_object, max_size)
            sub_folder_sum = get_folder_structure_total_size(file_object)
            # update sums
            sum_of_curr_folder += sub_folder_sum
            accumulated_sum += sub_accumulated
    # return accumulated sum, add curr folder if small enough
    return accumulated_sum + int(sum_of_curr_folder <= max_size) * sum_of_curr_folder


def find_smallest_directory_larger_than(folder_structure: FolderStructure, needed_size: int) -> int:
    """find the size of the smallest directory that is bigger than needed size"""
    current_best = get_folder_structure_total_size(folder_structure=folder_structure)

    for file_object in folder_structure.values():
        # only directories matter ! no file sizes
        if type(file_object) == dict:
            # update best based on the recursion through sub-folders
            sub_smallest_size = find_smallest_directory_larger_than(file_object, needed_size)
            if abs(needed_size) <= sub_smallest_size < current_best:
                current_best = sub_smallest_size

            # update best based on current folder size
            current_folder_total = get_folder_structure_total_size(file_object)
            if abs(needed_size) <= current_folder_total < current_best:
                current_best = current_folder_total
    return current_best




class Test2022Day07(unittest.TestCase):
    test_expected_folder_structure = {
        "a":     {
            "e":     {
                "i": 584,
            },
            "f":     29116,
            "g":     2557,
            "h.lst": 62596,
        },
        "b.txt": 14848514,
        "c.dat": 8504156,
        "d":     {
            "j":     4060174,
            "d.log": 8033020,
            "d.ext": 5626152,
            "k":     7214296,
        },
    }

    def test_get_folder_structure_at_path(self):
        for path, resulting_structure in [
            ([], self.test_expected_folder_structure),
            (["a"], self.test_expected_folder_structure["a"]),
            (["d"], self.test_expected_folder_structure["d"]),
            (["a", "e"], self.test_expected_folder_structure["a"]["e"]),
        ]:
            with self.subTest(msg=f'path: {path}'):
                self.assertEqual(get_folder_structure_at_path(
                    folder_structure=self.test_expected_folder_structure,
                    path=path
                ), resulting_structure)

    def test_parse_folder_structure(self):
        folder_structure = parse_folder_structure("data/07-test.txt")
        self.assertDictEqual(folder_structure, self.test_expected_folder_structure)

    def test_get_folder_structure_total_size(self):
        for folder_structure, total_size in [
            (self.test_expected_folder_structure, 48381165),
            (self.test_expected_folder_structure["a"], 94853),
            (self.test_expected_folder_structure["d"], 24933642),
            (self.test_expected_folder_structure["a"]["e"], 584),
        ]:
            with self.subTest(msg=f'size: {total_size}'):
                self.assertEqual(get_folder_structure_total_size(folder_structure), total_size)

    def test_find_size_of_small_directories(self):
        self.assertEqual(find_size_of_small_directories(self.test_expected_folder_structure), 95437)

    def test_find_smallest_directory_larger_than(self):
        total_size = get_folder_structure_total_size(self.test_expected_folder_structure)
        smallest = find_smallest_directory_larger_than(
            folder_structure=self.test_expected_folder_structure,
            needed_size=TOTAL_FS_SIZE - total_size - UPDATE_NEEDED_SIZE)
        self.assertEqual(smallest, 24933642)


if __name__ == '__main__':
    print(">>> Start Main 07:")
    puzzle_folder_structure = parse_folder_structure("data/07.txt")
    puzzle_accumulated_smaller_size = find_size_of_small_directories(puzzle_folder_structure)
    puzzle_total_size = get_folder_structure_total_size(puzzle_folder_structure)
    print("Part 1): ", puzzle_accumulated_smaller_size)
    print("Part 2): ", find_smallest_directory_larger_than(
        folder_structure=puzzle_folder_structure,
        needed_size=TOTAL_FS_SIZE - puzzle_total_size - UPDATE_NEEDED_SIZE
    ))
    print("End Main 07<<<")
