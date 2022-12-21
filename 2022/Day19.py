import unittest
from copy import deepcopy
from typing import Dict, List, Tuple, Set, Union
from math import ceil

from helper.file import read_lines_as_list

Price = Dict[str, int]
RobotPrices = Dict[str, Dict[str, int]]
Robots = Dict[str, int]
Material = Dict[str, int]


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

    def collect_maximum_geodes(
            self,
            minutes_left: int = 24, materials: Material = None, current_robots: Robots = None,
    ) -> int:
        """use this blueprint to get the maximum amount of"""
        if materials is None:
            # set starting materials to zero
            materials: Material = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        if current_robots is None:
            # set starting robots to 1 ore bot
            current_robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
        if minutes_left == 1:
            return materials["geode"]

        # get list of possible things to buy and in how many rounds that may be
        possible_buys: List[Tuple[int, str]] = []
        for robot_type, robot_cost in self.robot_prices.items():
            if all(0 < current_robots[ore] for ore in robot_cost.keys()):
                # (cost - current material) / per_round, but at least 1 round
                possible_buys.append(
                    (max((ceil(max(robot_cost[ore] - materials[ore], 1) / current_robots[ore])) for ore in robot_cost.keys()), robot_type)
                )

        # get and finally return max produced geode
        max_produced_geodes: int = 0
        # iterate through every possible new generation and get sub max result
        for rounds_to_buy, robot_to_buy in possible_buys:
            assert rounds_to_buy >= 1
            # not enough time to buy new robot
            if rounds_to_buy >= minutes_left:
                return materials["geode"] + current_robots["geode"] * minutes_left
            # break if robots is bigger that maximum of one per round
            if current_robots[robot_to_buy] + 1 > self.max_of_material[robot_to_buy]:
                continue
            # use current robots to produce everything possibly for multiple rounds
            # add produced robot to next iteration and remove materials
            new_materials = dict_sub_dict(
                dict_add_dict(materials, current_robots, d2_multiplier=rounds_to_buy),  # new materials
                self.robot_prices[robot_to_buy]  # subtract price of current robot
            )
            new_robots: Robots = dict_add_dict(current_robots, {robot_to_buy: 1})
            # recursive call
            sub_produced = self.collect_maximum_geodes(
                minutes_left=minutes_left - rounds_to_buy,
                materials=new_materials,
                current_robots=new_robots,
            )
            if sub_produced > max_produced_geodes:
                max_produced_geodes = sub_produced

        return max_produced_geodes

    def get_quality_label(self) -> int:
        """quality label = id * largest geodes"""
        return self.blueprint_id * self.collect_maximum_geodes()


class Test2022Day19(unittest.TestCase):
    test_blueprints: List[Blueprint] = [Blueprint(line) for line in read_lines_as_list("data/19-test.txt")]

    def test_collect_maximum_geodes(self):
        for bp_id, geodes_produced in [
            (1, 9),
            (2, 12),
        ]:
            with self.subTest(msg=f'id: {bp_id}'):
                self.assertEqual(deepcopy(self.test_blueprints[bp_id - 1]).collect_maximum_geodes(), geodes_produced)

    # def test_bp_quality_label(self):
    #     for bp_id, quality_label in [
    #         (1, 9),
    #         (2, 24),
    #     ]:
    #         with self.subTest(msg=f'id: {bp_id}'):
    #             self.assertEqual(deepcopy(self.test_blueprints[bp_id - 1]).get_quality_label(), quality_label)


if __name__ == '__main__':
    print(">>> Start Main 19:")
    puzzle_input: List[Blueprint] = [Blueprint(line) for line in read_lines_as_list("data/19.txt")]
    print("Part 1): ", sum(blueprint.get_quality_label() for blueprint in puzzle_input))
    print("Part 2): ")
    print("End Main 19<<<")
