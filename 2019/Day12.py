import unittest
from parameterized import parameterized

# position of four moons [Io, Europa, Ganymede, Callisto]
puzzle_input =\
    "<x=5, y=13, z=-3>\
     <x=18, y=-7, z=13>\
     <x=16, y=3, z=4>\
     <x=0, y=8, z=8>"
# initial velocity is 0


def convert_string_to_tuple(inp: str):
    """convert input of form <x=...,y=...,z=...> to tuple (x,y,z)"""
    pos = inp.replace(' ', '').replace('\n', '').replace('<', '').replace('>', '')
    return tuple(int(x[x.find('=')+1:]) for x in pos.split(','))


def convert_list_of_coordinates_to_tuple(inp: str):
    """convert input <x=...><x=...><x=...> to list of tuples [(x,...)(x,...)(x,...)]"""
    return list(convert_string_to_tuple(pos) for pos in inp.replace(' ', '').replace('\n', '').split('><'))


def convert_tuple_to_string(inp: tuple):
    """convert input of form tuple (x,y,z) to a string '<x=...,y=...,z=...>'"""
    return "<" + "".join(map(lambda sign, val: sign + "=" + str(val) + ",", ['x', 'y', 'z'], inp))[:-1] + ">"


def convert_list_of_tuples_to_string(inp: list):
    """convert list of tuples [(x,...)(x,...)(x,...)] to a string <x=...><x=...><x=...>"""
    return "".join(convert_tuple_to_string(val) for val in inp)


def convert_pos_vel_string_to_tuples(inp: str):
    """convert string of type pos=<>, vel=<> to two lists of tuples"""
    pos = []
    vel = []
    for d in inp.split(">"):
        if d.startswith('pos'):
            pos.append(d)
        elif d.startswith(', vel'):
            vel.append(d[2:])
    pos = [convert_string_to_tuple(p.replace('pos=', '') + '>') for p in pos]
    vel = [convert_string_to_tuple(v.replace('vel=', '') + '>') for v in vel]
    return pos, vel


# in each time step:
# 1. update v of every moon by applying gravity
# gravity is between pair of moons and
# axis gravity changes exactly +1 or -1 depending on the respective different position of the pair
def update_velocity(moon, other_positions, velocity):
    """update current moons velocity based on other velocities"""
    for other in other_positions:
        velocity = tuple(
            velocity[i] + (1 if other[i] > moon[i] else (-1 if other[i] < moon[i] else 0)) for i in range(len(velocity))
        )
    return velocity


# 2. update positions of all moons using velocity
def update_positions(pos, vel):
    """add current velocity to current position"""
    return tuple(map(lambda x, v: x + v, pos, vel))


def get_kinetic_energy(vel: tuple):
    """kin E is sum of abs val of velocity"""
    return sum(abs(x) for x in vel)


def get_potential_energy(pos: tuple):
    """pot E is sum of absolut values of position"""
    return sum(abs(x) for x in pos)


def simulate_t_time_steps(init_positions: list, init_velocities=None, time_steps=100):
    """simulate t time steps given list of tuples of position and velocity"""
    total_energy = 0
    if init_velocities is None:
        init_velocities = [(0,)*len(init_positions[0])]*len(init_positions)
    positions = init_positions
    velocities = init_velocities
    for t in range(time_steps):
        for i, moon in enumerate(positions):
            velocities[i] = update_velocity(moon, positions, velocities[i])
        for i in range(len(positions)):
            positions[i] = update_positions(positions[i], velocities[i])

    for i in range(len(positions)):
        total_energy += get_kinetic_energy(velocities[i]) * get_potential_energy(positions[i])

    return positions, velocities, total_energy


def least_common_multiple(list_of_divisors: list):
    """calculate lcm of a list"""
    from math import gcd
    lcm = list_of_divisors[0]
    for i in list_of_divisors[1:]:
        lcm = lcm * i // gcd(lcm, i)
    return lcm


def find_previously_match(init_positions: list, init_velocities=None):
    """Simulate time steps until there is a state that was previously seen"""
    # thanks to SO, dimensions x,y,z are independent! brute force did not work
    dimension = len(init_positions[0])
    dim_period = [0]*dimension
    if init_velocities is None:
        init_velocities = [(0,)*len(init_positions[0])]*len(init_positions)
    positions = init_positions
    velocities = init_velocities
    for d in range(dimension):
        seen_states = []
        positions_d = tuple(p[d] for p in positions)
        velocities_d = tuple(v[d] for v in velocities)
        while True:
            seen_states.append((positions_d + velocities_d))
            velocities_d = tuple(velocities_d[i] + sum(1 if other > current else (-1 if other < current else 0) for other in positions_d) for i, current in enumerate(positions_d))
            positions_d = tuple(positions_d[i] + velocities_d[i] for i in range(len(positions_d)))
            if (positions_d + velocities_d) in seen_states:
                dim_period[d] = len(seen_states)
                break
    # return least common multiple
    return least_common_multiple(dim_period)


class Test2019Day12(unittest.TestCase):
    @parameterized.expand([
        [0,  "pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>"],
        [1,  "pos=<x= 2, y=-1, z= 1>, vel=<x= 3, y=-1, z=-1>pos=<x= 3, y=-7, z=-4>, vel=<x= 1, y= 3, z= 3>pos=<x= 1, y=-7, z= 5>, vel=<x=-3, y= 1, z=-3>pos=<x= 2, y= 2, z= 0>, vel=<x=-1, y=-3, z= 1>"],
        [5,  "pos=<x=-1, y=-9, z= 2>, vel=<x=-3, y=-1, z= 2>pos=<x= 4, y= 1, z= 5>, vel=<x= 2, y= 0, z=-2>pos=<x= 2, y= 2, z=-4>, vel=<x= 0, y=-1, z= 2>pos=<x= 3, y=-7, z=-1>, vel=<x= 1, y= 2, z=-2>"],
        [10, "pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>"],
    ])
    def test_pos_vel_after_time_steps(self, time_step, result):
        example_input = convert_list_of_coordinates_to_tuple("<x=-1, y=0, z=2><x=2, y=-10, z=-7><x=4, y=-8, z=8><x=3, y=5, z=-1>")
        self.assertEqual(simulate_t_time_steps(example_input, time_steps=time_step)[:2], convert_pos_vel_string_to_tuples(result))

    def test_energy_after_time_steps(self):
        example_input = convert_list_of_coordinates_to_tuple("< x = -8, y = -10, z = 0 >< x = 5, y = 5, z = 10 >< x = 2, y = -7, z = 3 >< x = 9, y = -8, z = -3 >")
        self.assertEqual(simulate_t_time_steps(example_input, time_steps=100)[2], 1940)

    @parameterized.expand([
        ["<x=-1, y=0, z=2><x=2, y=-10, z=-7><x=4, y=-8, z=8><x=3, y=5, z=-1>", 2772],
        ["<x=-8, y=-10, z=0><x=5, y=5, z=10><x=2, y=-7, z=3><x=9, y=-8, z=-3>", 4686774924],
    ])
    def test_find_match(self, string_input, t):
        example_input = convert_list_of_coordinates_to_tuple(string_input)
        self.assertEqual(find_previously_match(example_input), t)


if __name__ == '__main__':
    print(">>> Start Main 12:")
    print("Part 1):")
    print(simulate_t_time_steps(convert_list_of_coordinates_to_tuple(puzzle_input), time_steps=1000)[2])
    print("Part 2):")
    print("final value: 271442326847376")
    print(find_previously_match(convert_list_of_coordinates_to_tuple(puzzle_input)))
    print("End Main 12<<<")
