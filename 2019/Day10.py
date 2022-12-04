import unittest
import math

from helper.tuple import tuple_dot_tuple, tuple_euclidean_norm, tuple_subtract_tuple

puzzle_input = [".###..#######..####..##...#",
                "########.#.###...###.#....#",
                "###..#...#######...#..####.",
                ".##.#.....#....##.#.#.....#",
                "###.#######.###..##......#.",
                "#..###..###.##.#.#####....#",
                "#.##..###....#####...##.##.",
                "####.##..#...#####.#..###.#",
                "#..#....####.####.###.#.###",
                "#..#..#....###...#####..#..",
                "##...####.######....#.####.",
                "####.##...###.####..##....#",
                "#.#..#.###.#.##.####..#...#",
                "..##..##....#.#..##..#.#..#",
                "##.##.#..######.#..#..####.",
                "#.....#####.##........#####",
                "###.#.#######..#.#.##..#..#",
                "###...#..#.#..##.##..#####.",
                ".##.#..#...#####.###.##.##.",
                "...#.#.######.#####.#.####.",
                "#..##..###...###.#.#..#.#.#",
                ".#..#.#......#.###...###..#",
                "#.##.#.#..#.#......#..#..##",
                ".##.##.##.#...##.##.##.#..#",
                "#.###.#.#...##..#####.###.#",
                "#.####.#..#.#.##.######.#..",
                ".#.#####.##...#...#.##...#."]

test_input = [".#..##.###...#######", "##.############..##.", ".#.######.########.#", ".###.#######.####.#.",
              "#####.##.#.##.###.##", "..#####..#.#########", "####################", "#.####....###.#.#.##",
              "##.#################", "#####.##.###..####..", "..######..##.#######", "####.##.####...##..#",
              ".#####..#.######.###", "##...#.##########...", "#.##########.#######", ".####.#.###.###.#.##",
              "....##.##.###..#####", ".#.#.###########.###", "#.#.#.#####.####.###", "###.##.####.##.#..##"]


def two_d_cross_product(x, y):
    """calculate cross-product in 2D"""
    return x[0] * y[1] - y[0] * x[1]


def get_arc_value(x, y):
    """get arc between two vectors"""
    if len(x) != len(y):
        raise Exception("Sizes of tuples do not match.")
    norm = tuple_euclidean_norm(x) * tuple_euclidean_norm(y)
    scalar_prod = tuple_dot_tuple(x, y)
    return format(math.degrees(math.acos(scalar_prod / norm)), '.9f')


def get_two_d_arc_tan_value(x, y):
    """get arc between two 2D vectors from 0 to 360"""
    return format(math.degrees(math.atan2(x[1], x[0]) - math.atan2(y[1], y[0])), '.4f')


def get_asteroid_coordinates(star_map):
    """get a list of asteroid coordinates"""
    asteroid_list = []
    for y, row in enumerate(star_map):
        for x, item in enumerate(row):
            if item == "#":
                asteroid_list.append((x, y))
    return asteroid_list


def get_location_value(star_map):
    """Get the value per location"""
    asteroid_list = get_asteroid_coordinates(star_map)
    value_map = list([list(-1 for _ in row) for row in star_map])
    seen_map = list([list({} for _ in row) for row in star_map])
    for asteroid in asteroid_list:
        # dict with arcs in which asteroids are seen with list for each direction with closest to furthest
        arc_dict = {}
        for other in asteroid_list:
            if other != asteroid:
                # get distance and calculate arc in degrees relative to (0, -1) [up] in 360 degrees
                distance_vec = tuple_subtract_tuple(other, asteroid)
                distance = tuple_euclidean_norm(distance_vec)
                arc = get_two_d_arc_tan_value(distance_vec, (0, -1))
                if arc in arc_dict.keys():
                    # save them with their distance into the list
                    arc_dict[arc].append((distance, other))
                else:
                    arc_dict[arc] = list([(distance, other)])
        # count different keys in dict and change value at position
        value_map[asteroid[1]][asteroid[0]] = len(arc_dict.keys())
        seen_map[asteroid[1]][asteroid[0]] = arc_dict
    # return . instead of -1 and number for everything else, make sure to space values
    return list(["".join(str(value) + " " if value >= 0 else ". " for value in row)[:-1] for row in value_map]), seen_map


def get_best_location(star_map):
    location_values, arc_values = get_location_value(star_map)
    location_values = list(
        [list(int(value) if value != '.' else -1 for value in row.split(' ')) for row in location_values])
    best_coord = ()
    best_value = 0
    for y, row in enumerate(location_values):
        for x, value in enumerate(row):
            if value > best_value:
                best_value = value
                best_coord = (x, y)
    return best_coord, best_value, arc_values[best_coord[1]][best_coord[0]]


def get_nth_vaporized(station_arc_values, n):
    """get the nth vaporized asteroid"""
    # transform dict to tuple to iterate more easily
    station_arc_values_tuple = []
    for key in station_arc_values.keys():
        station_arc_values_tuple.append(((float(key) + 360) % 360, station_arc_values[key]))
    station_arc_values_tuple = sorted(station_arc_values_tuple)
    index = 0
    i = 1
    while True:
        if len(station_arc_values_tuple[index][1]) > 0:
            # return if end
            if i == n:
                return station_arc_values_tuple[index][1][-1][1]
            # remove the closest item from list (last)
            station_arc_values_tuple[index][1].pop(-1)
        index += 1 % (len(station_arc_values_tuple) - 1)
        i += 1


class Test2019Day10(unittest.TestCase):
    def test_get_asteroid_coordinates(self):
        for star_map, coord_list in [
            [["."], []],
            [["#"], [(0, 0)]],
            [[".#", ".#", ".#"], [(1, 0), (1, 1), (1, 2)]],
        ]:
            with self.subTest():
                self.assertListEqual(get_asteroid_coordinates(star_map), coord_list)

    def test_detections(self):
        for inp, best in [
            [[".#", ".#", ".#"], [". 1", ". 2", ". 1"]],
            [["...", "###"], [". . .", "1 2 1"]],
            [[".#..#", ".....", "#####", "....#", "...##"],
             [". 7 . . 7", ". . . . .", "6 7 7 7 5", ". . . . 7", ". . . 8 7"]]
        ]:
            with self.subTest():
                self.assertListEqual(get_location_value(inp)[0], best)

    def test_output_best_position(self):
        for inp, best in [
            [[".#", ".#", ".#"], ((1, 1), 2)],
            [[".#..#", ".....", "#####", "....#", "...##"], ((3, 4), 8)],
            [["......#.#.", "#..#.#....", "..#######.", ".#.#.###..", ".#..#.....", "..#....#.#", "#..#....#.",
              ".##.#..###", "##...#..#.", ".#....####"], ((5, 8), 33)],
            [["#.#...#.#.", ".###....#.", ".#....#...", "##.#.#.#.#", "....#.#.#.", ".##..###.#", "..#...##..",
              "..##....##", "......#...", ".####.###."], ((1, 2), 35)],
            [[".#..#..###", "####.###.#", "....###.#.", "..###.##.#", "##.##.#.#.", "....###..#", "..#.#..#.#",
              "#..#.#.###", ".##...##.#", ".....#.#.."], ((6, 3), 41)],
            [test_input.copy(), ((11, 13), 210)],
            [puzzle_input.copy(), ((17, 23), 296)]
        ]:
            with self.subTest():
                self.assertTupleEqual(get_best_location(inp)[:-1], best)

    def test_nth_kill(self):
        best_stations_arcs = get_best_location(test_input.copy())[2]
        self.assertTupleEqual(get_nth_vaporized(best_stations_arcs.copy(), 1), (11, 12))
        self.assertTupleEqual(get_nth_vaporized(best_stations_arcs.copy(), 10), (12, 8))
        self.assertTupleEqual(get_nth_vaporized(best_stations_arcs.copy(), 200), (8, 2))


if __name__ == '__main__':
    print(">>> Start Main 10:")
    print("Part 1):")
    coord, value, arcs = get_best_location(puzzle_input)
    print("Best one at {} with a vision score of {}".format(coord, value))
    print("Part 2):")
    print("200th position will be: ", get_nth_vaporized(arcs, 200))
    print("End Main 10<<<")
