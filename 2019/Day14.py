import unittest
from parameterized import parameterized
import math
import copy

puzzle_input = ["14 LQGXD, 6 TDLQ => 9 VGLV", "1 WBQF, 2 JZKMJ => 5 TRSK", "5 MGHZ, 5 ZLDQF => 8 HMVG",
                "1 JWQH, 1 QFBC, 2 ZXVNM => 8 JFJZH", "8 QTPX, 8 LDLWS => 6 NVZPS", "2 QPWF, 1 PRWSM => 5 WHWF",
                "1 QPWF, 8 LDLWS => 5 LZBQ", "127 ORE => 1 MDPJB", "4 WHWF => 4 KQHW", "1 QBCKX, 3 TMTH => 4 WLFTZ",
                "15 NPMPT, 4 TMTH => 6 QFBC", "12 MDPJB => 9 PRWSM",
                "5 QXHFH, 3 LCDVR, 24 MWFP, 1 MSFV, 1 BPDJL, 3 LQGXD, 2 DVGW => 2 KCPSH",
                "6 FPZXN, 1 FQSK, 3 TMTH => 1 FBHW", "25 PRWSM => 1 MGHZ", "6 XWKXC, 5 TMTH, 1 PZTGX => 6 NTQZ",
                "3 BPDJL, 3 DJWCL, 2 JZKMJ => 7 MWFP", "5 JFJZH => 3 DJWCL", "22 WRNJ, 12 TRSK => 5 TBGJC",
                "3 HKWP => 1 PDRN", "3 JWQH => 5 JZKMJ", "4 WBQF => 2 BJNS", "1 GNBQ => 9 FQSK",
                "8 HMVG, 1 HQHD => 5 NJFNC", "7 QBCKX, 1 FQSK => 9 NDCQ",
                "3 XWKXC, 7 QFBC, 3 GPFRS, 2 LPQZ, 2 LQGXD, 20 LZKM, 1 QRTH => 8 TDTKT", "1 QTPX => 3 LPQZ",
                "2 QGVQC, 14 LDLWS => 1 NPMPT", "1 QRTH, 7 BPDJL => 7 XWKXC", "9 WLFTZ, 8 TDLQ => 6 GKPK",
                "4 GNBQ => 3 QXHFH", "3 TBGJC, 1 LPQZ => 3 DVGW", "3 NDCQ, 1 KGZT => 7 FPZXN",
                "36 WLFTZ, 1 KCPSH, 1 GKPK, 1 TDTKT, 3 CSPFK, 27 JZKMJ, 5 VGLV, 39 XWKXC => 1 FUEL",
                "115 ORE => 7 QGVQC", "21 NTQZ, 11 HQHD, 33 JFJZH, 3 NJFNC, 3 MSFV, 1 TRSK, 7 WRNJ => 9 CSPFK",
                "3 DVGW => 4 TDLQ", "5 FPZXN => 6 WRNJ", "10 TSDLM, 17 XDKP, 3 PDRN => 2 HQHD", "1 PCWS => 3 PZTGX",
                "2 QXHFH => 5 JWQH", "17 KQHW => 2 WBQF", "139 ORE => 5 LDLWS", "3 TSDLM => 9 KGZT",
                "16 NPMPT => 3 QTPX", "3 DVGW, 5 KVFMS, 3 WLFTZ => 6 GPFRS", "1 PZTGX, 2 LCDVR, 13 TBGJC => 6 LZKM",
                "5 ZXVNM, 2 QXHFH => 4 MSFV", "4 XDKP, 7 FBHW, 2 PCWS => 3 LCDVR", "3 TRSK => 7 KVFMS",
                "10 LDLWS => 9 TMTH", "2 TBGJC => 6 LQGXD", "2 TRSK => 6 ZXVNM", "4 KQHW, 1 NVZPS => 8 ZLDQF",
                "2 LZBQ => 4 QBCKX", "7 QBCKX => 6 TSDLM", "152 ORE => 3 QPWF", "2 TSDLM, 8 WHWF => 3 HKWP",
                "19 FQSK => 8 QRTH", "19 QTPX => 3 GNBQ", "4 PDRN, 12 HKWP, 4 PCWS => 3 XDKP",
                "6 LZBQ, 19 BJNS => 5 BPDJL", "5 HKWP, 6 NVZPS => 3 PCWS"]


def parse_dep_graph(string_dep_graph):
    """given list of dependency strings, return list of tuples of dicts for each dependency"""
    dependencies = []
    for graph_dependency in string_dep_graph:
        # "x A, y B => z C" -> split right and left
        dependency = ()
        for graph_ingredients in graph_dependency.split("=>"):
            ingredients = {}
            for ingredient in graph_ingredients.split(","):
                g_ingr = ingredient.strip().split(" ")
                ingredients[g_ingr[1]] = int(g_ingr[0])
            dependency += tuple(list([ingredients]))
        dependencies.append(dependency)
    return dependencies


def find_product_in_graph(dependency_graph, product):
    """Find all the nodes in the graph that have product on the right hand side"""
    solutions = []
    for dependency in dependency_graph:
        for key in dependency[1].keys():
            if key == product:
                solutions.append(dependency)
    return solutions


def solve_graph(dep_graph, goal="FUEL", start="ORE"):
    """Solve the dependecy graph, so goal only depends on start"""
    goal_nodes = find_product_in_graph(dep_graph, goal)
    if len(goal_nodes) > 1:
        raise Exception("There is more than one way to achieve the goal")
    elif len(goal_nodes) == 0:
        raise Exception("There is not a single node that can achieve the goal")
    else:
        current_goal_node = goal_nodes[0]
    # while there are some educts that aren't the start item or overproduction
    while any(start != key and current_goal_node[0][key] > 0 for key in current_goal_node[0].keys()):
        # dict may change size during execution, therefore work on a copy
        for key in list(current_goal_node[0].keys()):
            if key != start:
                possiple_solutions = find_product_in_graph(dep_graph, key)
                if len(possiple_solutions) < 1:
                    raise Exception("The key {} was not found in the dependency tree".format(key))
                elif len(possiple_solutions) > 1:
                    raise Exception("The key {} appears in more than one dependency path".format(key))
                else:
                    possiple_solution = possiple_solutions[0]
                    necessary_educt = current_goal_node[0][key]
                    possible_product = possiple_solution[1][key]
                    reaction_multiplicator = math.ceil(necessary_educt / possible_product)
                    overproduction = necessary_educt - (reaction_multiplicator * possible_product)
                    for educt, quantity in possiple_solution[0].items():
                        # increase count of educt in goal node, or add it with the necessary quantity
                        if educt not in current_goal_node[0]:
                            current_goal_node[0][educt] = 0
                        current_goal_node[0][educt] += reaction_multiplicator * quantity
                    # if all educts are added remove product from goal
                    current_goal_node[0].pop(key)
                    # re-add overproduction of product, to have the overflow for the possible next time
                    if overproduction < 0:
                        current_goal_node[0][key] = overproduction
    # return amount of ore needed
    try:
        ore_amount = current_goal_node[0][start]
    except KeyError:
        ore_amount = 0
    return ore_amount, current_goal_node


def max_fuel_for_ore(init_graph, ore_amount=1000000000000, goal="FUEL", start="ORE"):
    """Get as many fuel with provided amount of ore"""
    graph = copy.deepcopy(init_graph)
    goal_amount = 0
    start_amount = 0
    ore_to_fuel_amount, _ = solve_graph(copy.deepcopy(graph), goal, start)
    # find goal node
    goal_nodes = find_product_in_graph(graph.copy(), goal)
    if len(goal_nodes) > 1:
        raise Exception("There is more than one way to achieve the goal")
    else:
        goal_node = goal_nodes[0]
        del goal_nodes
    graph.remove(goal_node)
    new_goal_node = ({}, {})
    # as long as there is not to much of start
    while start_amount <= ore_amount:
        # it should be safe to add multiple fuels at once, as long as there is
        # enough time to get rid of the overproduction
        multiplicator = int(0.5 * ((ore_amount - start_amount) / ore_to_fuel_amount))
        multiplicator = multiplicator if multiplicator >= 10 else 1
        # append original goal with multiplicator into new goal node
        for side_i in range(len(goal_node)):
            for key, value in goal_node[side_i].items():
                if key in new_goal_node[side_i]:
                    new_goal_node[side_i][key] += value * multiplicator
                else:
                    new_goal_node[side_i][key] = value * multiplicator
        new_graph = graph.copy() + list([new_goal_node])
        amount, new_goal_node = solve_graph(copy.deepcopy(new_graph), goal, start)
        # goal and start will be readded in the next iteration, so they can be removed.
        # currently just keep all the overproduction
        if start in new_goal_node[0]:
            new_goal_node[0].pop(start)
        if goal in new_goal_node[1]:
            new_goal_node[1].pop(goal)
        start_amount += amount
        goal_amount += multiplicator
    return goal_amount - 1


class Test2019Day14(unittest.TestCase):
    @parameterized.expand([
        [["9 ORE => 2 A"], [({"ORE": 9}, {"A": 2})]],
        [["9 ORE, 100 B => 2 A"], [({"ORE": 9, "B": 100}, {"A": 2})]],
        [["9 ORE => 2 A, 10 B, 100 C"], [({"ORE": 9}, {"A": 2, "B": 10, "C": 100})]],
        [["9 ORE => 2 A", "9 ORE => 2 A"], [({"ORE": 9}, {"A": 2}), ({"ORE": 9}, {"A": 2})]],
    ])
    def test_parse_dep_graph(self, dep, result):
        self.assertListEqual(parse_dep_graph(dep), result)

    @parameterized.expand([
        ["X", [({"ORE": 9}, {"A": 2, "B": 10, "C": 100})], []],
        ["C", [({"ORE": 9}, {"A": 2, "B": 10, "C": 100})], [({"ORE": 9}, {"A": 2, "B": 10, "C": 100})]],
        ["FUEL", [({"ORE": 9}, {"FUEL": 2}), ({"ORE": 9}, {"A": 2, "B": 10, "C": 100}), ({"ORE": 9}, {"A": 2})], [({"ORE": 9}, {"FUEL": 2})]],
    ])
    def test_find_node(self, item, tree, result):
        self.assertListEqual(find_product_in_graph(tree, item), result)

    @parameterized.expand([
        [10, ["1 ORE => 1 A", "10 A => 1 FUEL"]],
        [165,
         ["9 ORE => 2 A", "8 ORE => 3 B", "7 ORE => 5 C", "3 A, 4 B => 1 AB", "5 B, 7 C => 1 BC", "4 C, 1 A => 1 CA",
          "2 AB, 3 BC, 4 CA => 1 FUEL"]],
        [13312,
         ["157 ORE => 5 NZVS", "165 ORE => 6 DCFZ", "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
          "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ", "179 ORE => 7 PSHF", "177 ORE => 5 HKGWZ", "7 DCFZ, 7 PSHF => 2 XJWVT",
          "165 ORE => 2 GPVTF", "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"]],
        [180697, ["2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG", "17 NVRVD, 3 JNWZP => 8 VPVL",
                  "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL", "22 VJHF, 37 MNCFX => 5 FWMGM",
                  "139 ORE => 4 NVRVD", "144 ORE => 7 JNWZP", "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC",
                  "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV", "145 ORE => 6 MNCFX", "1 NVRVD => 8 CXFTF",
                  "1 VJHF, 6 MNCFX => 4 RFSQX", "176 ORE => 6 VJHF"]],
        [2210736, ["171 ORE => 8 CNZTR", "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL",
                   "114 ORE => 4 BHXH", "14 VRPVC => 6 BMBT",
                   "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
                   "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT",
                   "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
                   "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW", "5 BMBT => 4 WPTQ",
                   "189 ORE => 9 KTJDG", "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP", "12 VRPVC, 27 CNZTR => 2 XDBXC",
                   "15 KTJDG, 12 BHXH => 5 XCVML", "3 BHXH, 2 VRPVC => 7 MZWV", "121 ORE => 7 VRPVC",
                   "7 XCVML => 6 RJRHP", "5 BHXH, 4 VRPVC => 5 LTCX"]],
    ])
    def test_ore_to_fuel_ratio(self, fuel, dependencies):
        self.assertEqual(fuel, solve_graph(parse_dep_graph(dependencies))[0])

    @parameterized.expand([
        [100000, ["1 ORE => 1 A", "10000000 A => 1 FUEL"]],
        [82892753,
         ["157 ORE => 5 NZVS", "165 ORE => 6 DCFZ", "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
          "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ", "179 ORE => 7 PSHF", "177 ORE => 5 HKGWZ", "7 DCFZ, 7 PSHF => 2 XJWVT",
          "165 ORE => 2 GPVTF", "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"]],
        [5586022, ["2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG", "17 NVRVD, 3 JNWZP => 8 VPVL",
                  "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL", "22 VJHF, 37 MNCFX => 5 FWMGM",
                  "139 ORE => 4 NVRVD", "144 ORE => 7 JNWZP", "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC",
                  "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV", "145 ORE => 6 MNCFX", "1 NVRVD => 8 CXFTF",
                  "1 VJHF, 6 MNCFX => 4 RFSQX", "176 ORE => 6 VJHF"]],
        [460664, ["171 ORE => 8 CNZTR", "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL",
                   "114 ORE => 4 BHXH", "14 VRPVC => 6 BMBT",
                   "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
                   "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT",
                   "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
                   "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW", "5 BMBT => 4 WPTQ",
                   "189 ORE => 9 KTJDG", "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP", "12 VRPVC, 27 CNZTR => 2 XDBXC",
                   "15 KTJDG, 12 BHXH => 5 XCVML", "3 BHXH, 2 VRPVC => 7 MZWV", "121 ORE => 7 VRPVC",
                   "7 XCVML => 6 RJRHP", "5 BHXH, 4 VRPVC => 5 LTCX"]],
    ])
    def test_trillion_to_fuel_ratio(self, fuel, dependencies):
        self.assertEqual(fuel, max_fuel_for_ore(parse_dep_graph(dependencies)))


if __name__ == '__main__':
    print(">>> Start Main 14:")
    print("Part 1):")
    print(solve_graph(parse_dep_graph(puzzle_input))[0])
    print("Part 2):")
    print(max_fuel_for_ore(parse_dep_graph(puzzle_input)))
    print("End Main 14<<<")
