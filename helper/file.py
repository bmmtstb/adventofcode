"""
General file handling functions.

Most day solutions require reading some sort of list from a file.
"""

from typing import List, Union, Callable


def load_file_and_split(
    filepath: str, separator: str = "\n", instance_type: type = str
) -> List[Union[int, str, float]]:
    """Read a file and split it at every occurrence of separator.
    The separated instances will be cast to instanceType.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        lines = [instance_type(val) for val in file.read().split(separator)]
    return lines


def read_lines_as_list(
    filepath, instance_type: Union[type, Callable] = str, split: str = None
):
    """Reads the file at filepath.
    Splits "every" line into substrings if provided.
    Additionally, casts the value(s) of all (possibly split lines) to the given type.
    """
    data = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file.readlines():
            line = line.replace("\n", "")
            if split == "every":
                data.append([instance_type(val) for val in line])
            elif split:
                data.append([instance_type(val) for val in line.split(split)])
            else:
                data.append(instance_type(line))
    return data
