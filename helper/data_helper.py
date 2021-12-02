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
