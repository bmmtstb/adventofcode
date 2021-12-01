def read_lines_as_list(filepath, t: type = str):
    """reads the file at filepath"""
    data = []
    with open(filepath) as file:
        for line in file.readlines():
            data.append(t(line.replace("\n", "")))
    return data
