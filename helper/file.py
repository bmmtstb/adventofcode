from typing import Dict, List, Tuple, Set


def load_file(filepath: str) -> List[str]:
    """read a file, return a list of all lines"""
    with open(filepath) as file:
        lines = file.readlines()
    return lines


def load_file_split(filepath: str, sep: str = "\n") -> List[str]:
    """read a file and split it at every occurrence of sep"""
    with open(filepath) as file:
        lines = file.read().split(sep)
    return lines


