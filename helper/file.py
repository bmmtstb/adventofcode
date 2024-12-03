"""
General file handling functions.

Most day solutions require reading some sort of list from a file.
"""

from typing import List, TypeVar, Union, Callable

InstanceType = TypeVar("InstanceType", bound=type)


def load_file_and_split(
    fp: str,
    sep: str = "\n",
    inst: Union[InstanceType, Callable[[any], InstanceType]] = str,
) -> List[InstanceType]:
    """
    Read a file and split it at every occurrence of separator.
    The separated instances will be cast to instanceType.

    Args:
        fp (str): Path to the file.
        sep (str, optional): String at which to split the raw string. Defaults to "\n".
        inst (InstanceType, optional): Type to cast the individual splits to. Defaults to str.

    Returns:
        A list containing the split instances of the raw data.
    """
    with open(fp, "r", encoding="utf-8") as file:
        lines = [inst(val) for val in file.read().split(sep)]
    return lines


def read_lines_as_list(
    fp,
    inst: Union[InstanceType, Callable[[any], InstanceType]] = str,
    split: str = None,
) -> list[Union[InstanceType, list[InstanceType]]]:
    """Reads the file at filepath.
    Splits "every" line into substrings if provided.
    Additionally, casts the value(s) of all (possibly split lines) to the given type.

    Args:
        fp (str): Path to the file.
        inst (InstanceType, optional): Type to cast the individual splits to. Defaults to str.
        split (str, optional): String at which to split the raw string. Defaults to "\n".

    Returns:
        A list containing the split instances of the raw data.
        Either as a list of instances, or a list of lists of instances.
    """
    data = []
    with open(fp, "r", encoding="utf-8") as file:
        for line in file.readlines():
            line = line.replace("\n", "")
            if split == "every":
                data.append([inst(val) for val in line])
            elif split:
                data.append([inst(val) for val in line.split(split)])
            else:
                data.append(inst(line))
    return data
