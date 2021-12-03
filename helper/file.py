from typing import Dict, List, Tuple, Set


def load_file_split(filepath: str, sep: str = "\n") -> List[str]:
    """read a file and split it at every occurrence of sep"""
    with open(filepath) as file:
        lines = file.read().split(sep)
    return lines


def read_lines_as_list(filepath, t: type = str, split: str = None):
    """reads the file at filepath"""
    data = []
    if split and t != str:
        raise Exception("Bad parameters")
    with open(filepath) as file:
        for line in file.readlines():
            if split:
                data.append(line.replace("\n", "").split(split))
            else:
                data.append(t(line.replace("\n", "")))
    return data
