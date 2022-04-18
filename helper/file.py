from typing import List, Union


def load_file_and_split(filepath: str, sep: str = "\n", t: type = str) -> List[Union[int, str, float]]:
    """read a file and split it at every occurrence of sep"""
    with open(filepath) as file:
        lines = [t(val) for val in file.read().split(sep)]
    return lines


def read_lines_as_list(filepath, t: type = str, split: str = None):
    """reads the file at filepath, split a line into substrings if provided, casts to type"""
    data = []
    with open(filepath) as file:
        for line in file.readlines():
            line = line.replace("\n", "")
            if split == "every":
                data.append([t(val) for val in line])
            elif split:
                data.append([t(val) for val in line.split(split)])
            else:
                data.append(t(line))
    return data
