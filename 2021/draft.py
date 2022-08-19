def build_map(map, filler):
    w = len(map[0]) + 2
    new_map = []
    new_map.append([filler] * w)
    for line in map:
        new_map.append([filler] + line + [filler])
    new_map.append([filler] * w)
    return new_map


def get_neighbors(r, c, map, filler):
    bs = ""
    for rm in range(-1, 2):
        for cm in range(-1, 2):
            if r + rm < 0 or r + rm >= len(map) or c + cm < 0 or c + cm >= len(map[0]):
                bs += str(filler)
            else:
                bs += str(map[r + rm][c + cm])
    return 1 if alg[int(bs, 2)] == "#" else 0


data = open("data/20.txt").read().strip().split("\n\n")
alg = data.pop(0)
map = [[0 if j == "." else 1 for j in i] for i in data[0].split("\n")]

for i in range(1, 50 + 1):
    # determine state of infinite pixels
    filler = 1 if alg[0] == "#" and alg[-1] == "." and not i % 2 else 0
    map = build_map(map, filler)
    # iterate over map and find updates
    changes = {}
    for r in range(len(map)):
        for c in range(len(map[0])):
            changes[(r, c)] = get_neighbors(r, c, map, filler)
    # apply updates to map
    for r, c in changes:
        map[r][c] = changes[(r, c)]
    if i == 2:
        print(f"Part 1: {sum([val for sublist in map for val in sublist])}")
print(f"Part 2: {sum([val for sublist in map for val in sublist])}")
