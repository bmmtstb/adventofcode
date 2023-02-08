import unittest
from copy import deepcopy
from typing import Dict, List, Tuple, Set, Union
from math import ceil

from helper.file import read_lines_as_list

Price = Dict[str, int]
RobotPrices = Dict[str, Dict[str, int]]
Robots = Dict[str, int]
Material = Dict[str, int]


PRIORITY: Dict[str, int] = {
    "geode": 1,
    "obsidian": 2,
    "clay": 3,
    "ore": 4
}


def dict_add_dict(d1: Union[Material, Price], d2: Union[Material, Price], d2_multiplier: int = 1) -> Union[Material, Price]:
    """given materials add new ones (new instance)"""
    return {key: d1.get(key, 0) + d2_multiplier * d2.get(key, 0) for key in set(d1) | set(d2)}


def dict_sub_dict(d1: Union[Material, Price], d2: Union[Material, Price]) -> Union[Material, Price]:
    """given materials add new ones (new instance)"""
    return {key: d1.get(key, 0) - d2.get(key, 0) for key in set(d1) | set(d2)}


def dict_geq_dict(d1: Union[Material, Price], d2: Union[Material, Price]) -> bool:
    """returns whether there is more or equal in dict 1 than in 2"""
    return all(d1_value >= d2[d1_key] for d1_key, d1_value in d1.items() if d1_key in d2)


class Blueprint:
    def __init__(self, bp: str):
        bp_id, robot_prices_raw = bp[:-1].split(": ")
        # get id
        self.blueprint_id = int(bp_id[10:])
        # read prices for every robot type
        self.robot_prices: RobotPrices = {}

        robot_prices_raw = robot_prices_raw.split(". ")
        for robot_type_cost in robot_prices_raw:
            robot_type, cost = robot_type_cost.split(" robot costs ")
            robot_type = robot_type[5:]
            if " and " in cost:
                costs = cost.split(" and ")
            else:
                costs = [cost]
            robot_price: Price = {}
            for cost in costs:
                amount, ore_type = cost.split(" ")
                robot_price[ore_type] = int(amount)
            # set robot price
            self.robot_prices[robot_type] = robot_price

        # indirectly sets the maximum number of robots
        # at most N of this type are needed for one operation, therefore we will never need more than that robots
        self.max_of_material = {
            "ore": max(robot["ore"] for robot in self.robot_prices.values() if "ore" in robot),
            "clay": max(robot["clay"] for robot in self.robot_prices.values() if "clay" in robot),
            "obsidian": max(robot["obsidian"] for robot in self.robot_prices.values() if "obsidian" in robot),
            "geode": 24,  # or sth like int max
        }

    def get_possible_buys(self, current_robots: Robots, current_materials: Material) -> Dict[str, int]:
        """get a list of robots that can be bought with the number of rounds it takes to buy that robot"""
        possible_buys: Dict[str, int] = {}
        for robot_type, robot_cost in self.robot_prices.items():
            if all(0 < current_robots[ore] for ore in robot_cost.keys()):
                # skip if robots is bigger that maximum of one per round
                if current_robots[robot_type] + 1 > self.max_of_material[robot_type]:
                    continue
                # (cost - current material) / per_round, but at least 0 rounds, then add the 1 round of producing while building
                possible_buys[robot_type] = \
                    max((ceil(max(robot_cost[ore] - current_materials[ore], 0) / current_robots[ore])) for ore in robot_cost.keys()) + 1

        return possible_buys

    def collect_maximum_geodes(
            self,
            minutes_left: int = 24, materials: Material = None, current_robots: Robots = None,
    ) -> int:
        """use this blueprint to get the maximum amount of"""
        if materials is None:
            # set starting materials to zero
            materials: Material = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        if current_robots is None:
            # set starting robots to 1 ore robot
            current_robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}

        # calculate maximum amount of geodes in current branch =
        # build one geode robot every step until end + current geodes + one for every minute for every existing robot
        # using formular for sum from 1 to n = n(n+1) / 2
        theoretical_max_production: int = \
            materials["geode"] + \
            minutes_left * current_robots["geode"] + \
            int((minutes_left * (minutes_left + 1)) / 2)

        # get and finally return max produced geode
        max_produced_geodes: int = materials["geode"]

        # Get list of possible things to buy and in how many rounds that can be done.
        possible_buys = self.get_possible_buys(current_robots, materials)
        # Iterate through every possible new generation and get sub max result
        for robot_to_buy, rounds_to_material in possible_buys.items():
            # iff theoretical maximum is lower than or equal to max_produced_geodes, no need to check this whole branch
            # maximum is already reached
            if theoretical_max_production <= max_produced_geodes:
                return max_produced_geodes
            # not enough time to buy new robot
            if rounds_to_material >= minutes_left:
                assert minutes_left >= 0
                return max(materials["geode"] + current_robots["geode"] * minutes_left, max_produced_geodes)
            # only produce geode robots in the end
            if minutes_left < 5 and robot_to_buy != "geode":
                continue
            # use current robots to produce everything possibly for multiple rounds
            # add produced robot to next iteration and remove materials
            new_materials = dict_sub_dict(
                dict_add_dict(materials, current_robots, d2_multiplier=rounds_to_material),  # new materials
                self.robot_prices[robot_to_buy]  # subtract price of current robot from all materials
            )
            # recursive call
            sub_produced = self.collect_maximum_geodes(
                minutes_left=minutes_left - rounds_to_material,
                materials=new_materials,
                current_robots=dict_add_dict(current_robots, {robot_to_buy: 1}),  # add planned robot
            )
            # get max produced
            max_produced_geodes = max(max_produced_geodes, sub_produced)

        return max_produced_geodes

    def get_quality_label(self) -> int:
        """quality label = id * largest geodes"""
        return self.blueprint_id * self.collect_maximum_geodes()


class Test2022Day19(unittest.TestCase):
    test_blueprints: List[Blueprint] = [Blueprint(line) for line in read_lines_as_list("data/19-test.txt")]

    def test_dict_add_dict(self):
        empty = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        random = {'obsidian': 2, 'clay': 11, 'geode': 0, 'ore': 4}
        one_value = {"ore": 10}  # does not have to have all values
        for d1, d2, multiplier, result in [
            (empty, random, 1, random),
            (empty, random, 10, {'obsidian': 20, 'clay': 110, 'geode': 0, 'ore': 40}),
            (random, empty, 10, random),
            (empty, one_value, 1, {"ore": 10, "clay": 0, "obsidian": 0, "geode": 0}),
            (random, one_value, 5, {'obsidian': 2, 'clay': 11, 'geode': 0, 'ore': 54}),
        ]:
            with self.subTest(msg=f'd1:{d1}, d2: {d2}'):
                self.assertEqual(dict_add_dict(d1, d2, d2_multiplier=multiplier), result)

    def test_dict_sub_dict(self):
        empty = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        random = {'obsidian': 2, 'clay': 11, 'geode': 0, 'ore': 4}
        one_value = {"ore": 1}
        for d1, d2, result in [
            (random, empty, random),
            (random, one_value, {'obsidian': 2, 'clay': 11, 'geode': 0, 'ore': 3}),
            (random, random, empty)
        ]:
            with self.subTest(msg=f'd1:{d1}, d2: {d2}'):
                self.assertEqual(dict_sub_dict(d1, d2), result)

    def test_dict_geq_dict(self):
        empty = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        random = {'obsidian': 2, 'clay': 11, 'geode': 0, 'ore': 4}
        one_value = {"ore": 1}
        one_value_big = {"ore": 5}
        for d1, d2, result in [
            (random, empty, True),
            (random, one_value, True),
            (random, one_value_big, False),
            (one_value, empty, True),
            (one_value_big, empty, True),
        ]:
            with self.subTest(msg=f'd1:{d1}, d2: {d2}'):
                self.assertEqual(dict_geq_dict(d1, d2), result)

    def test_get_possible_buys(self):
        empty = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        random = {'obsidian': 2, 'clay': 11, 'geode': 0, 'ore': 0}
        one_value = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
        one_value_big = {"ore": 5, "clay": 0, "obsidian": 0, "geode": 0}
        two_values = {"ore": 1, "clay": 5, "obsidian": 0, "geode": 0}
        for robots, materials, buys in [
            (one_value, one_value_big, {"ore": 1, "clay": 1}),  # 1 round to build
            (empty, empty, {}),  # no production, no material
            (two_values, empty, {"ore": 5, "clay": 3, "obsidian": 4}),
            (one_value, random, {"ore": 5, "clay": 3}),
            (two_values, random, {"ore": 5, "clay": 3, "obsidian": 4}),
        ]:
            with self.subTest(msg=f'robots:{robots}, materials: {materials}'):
                bp = deepcopy(self.test_blueprints[0])
                self.assertEqual(bp.get_possible_buys(robots, materials), buys)

    def test_bp_max_geodes(self):
        for bp_id, max_geodes, minutes in [
            (1, 9, 24),
            (2, 12, 24),
            # (1, 56, 32),
            # (2, 62, 32),
        ]:
            with self.subTest(msg=f'id: {bp_id}, minutes: {minutes}'):
                self.assertEqual(deepcopy(self.test_blueprints[bp_id - 1]).collect_maximum_geodes(minutes_left=minutes), max_geodes)


if __name__ == '__main__':
    print(">>> Start Main 19:")
    puzzle_input: List[Blueprint] = [Blueprint(line) for line in read_lines_as_list("data/19.txt")]
    print("Part 1): ", sum(blueprint.get_quality_label() for blueprint in deepcopy(puzzle_input)))
    factors = [bp.collect_maximum_geodes(minutes_left=32) for bp in deepcopy(puzzle_input)[:3]]
    # 37367
    print("Part 2): ", factors, " multiply these")
    print("End Main 19<<<")
