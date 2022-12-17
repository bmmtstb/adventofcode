import unittest
from typing import Dict, List, Tuple, Set

from helper.file import read_lines_as_list

TunnelSystem = Dict[str, List[str]]
FlowRates = Dict[str, int]
TravelGuide = Dict[str, Dict[str, int]]
Edges = List[Tuple[str, str]]


def load_data(filepath: str) -> Tuple[TunnelSystem, FlowRates, FlowRates, Edges, TravelGuide]:
    """load values from file"""
    lines = read_lines_as_list(filepath=filepath, split="; ")
    tunnel: TunnelSystem = {}
    flows: FlowRates = {}
    edges: Edges = []
    for flow_rate, leading in lines:
        valve_name, flow_rate = flow_rate.split("=")
        valve_name = valve_name[6:8]
        if "valves" in leading:
            leading = leading[23:].split(", ")
        else:
            leading = [leading[22:]]
        tunnel[valve_name] = leading
        flows[valve_name] = int(flow_rate)
        for l in leading:
            edges.append((valve_name, l))

    travel_guide = get_from_to(edges, tunnel)
    non_zero_flows = {key: value for key, value in flows.items() if value > 0 or key == "AA"}
    return tunnel, flows, non_zero_flows, edges, travel_guide


def get_from_to(edges: Edges, tunnel: TunnelSystem) -> TravelGuide:
    """get the minimal travel amount to get from x to y"""
    travel_guide: TravelGuide = {key: {sub_key: int(1e10) for sub_key in tunnel.keys()} for key in tunnel.keys()}

    # floyd warshall algorithm: https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
    # set values of every direct edge
    for u, v in edges:
        travel_guide[u][v] = 1  # time to get from u to v on the edge (1 in every case)
    # set diagonal to zero
    for vertex in tunnel.keys():
        travel_guide[vertex][vertex] = 0
    # set all multistep distances
    for key_k in tunnel.keys():
        for key_i in tunnel.keys():
            for key_j in tunnel.keys():
                if travel_guide[key_i][key_j] > travel_guide[key_i][key_k] + travel_guide[key_k][key_j]:
                    travel_guide[key_i][key_j] = travel_guide[key_i][key_k] + travel_guide[key_k][key_j]
    assert all(all(sub_key_value < int(1e10) for sub_key_value in travel_guide[key].values()) for key in travel_guide.keys())
    return travel_guide


def get_max_released_pressure(
        travel_guide: TravelGuide, flows: FlowRates, current_node: str = "AA", minutes_left: int = 30,
        opened_valves: List[str] = None
) -> int:
    """starting at AA, compute the amount of max release pressure"""
    # replace default value
    if opened_valves is None:
        opened_valves: List[str] = []

    # get max possible flow over time
    max_flow_value = 0
    # loop all non zero keys
    for next_node in flows.keys():
        # skip already opened valves / nodes
        if next_node in opened_valves:
            continue
        # skip zero nodes
        if flows[next_node] == 0:
            continue

        # expect to open every node passed -> no zero nodes in list
        # this is the current time minus the time to get and open the node
        time_to_open_valve: int = travel_guide[current_node][next_node] + 1
        # break if there is no more time
        if time_to_open_valve > minutes_left:
            continue
        # flow times the total amount valve can be open for
        possible_flow_released = flows[next_node] * (minutes_left - time_to_open_valve)

        possible_flow_recursive = get_max_released_pressure(
            travel_guide=travel_guide, flows=flows,
            current_node=next_node,
            minutes_left=minutes_left - time_to_open_valve,
            opened_valves=opened_valves + [next_node],  # this one is opened too recursively
        )

        if possible_flow_released + possible_flow_recursive > max_flow_value:
            max_flow_value = possible_flow_released + possible_flow_recursive

    return max_flow_value


def get_max_released_pressure_two_person(
        travel_guide: TravelGuide, valve_flows: FlowRates,
        me_starting_node: str = "AA", elephant_starting_node: str = "AA",
        me_minutes_left: int = 26, elephant_minutes_left: int = 26,
        opened_valves: List[str] = None
) -> int:
    """
    starting with me and the elephant at AA with 26 minutes left, compute the amount of max release pressure
    returns the max flow value
    """
    # replace default value
    if opened_valves is None:
        opened_valves: List[str] = []

    # get max possible flow over time
    max_flow_value = 0

    if me_minutes_left >= elephant_minutes_left:
        # get next value for me
        # loop all non-zero keys
        for next_node in valve_flows.keys():
            # skip already opened valves / nodes
            if next_node in opened_valves:
                continue
            # skip zero nodes
            if valve_flows[next_node] == 0:
                continue

            # expect to open every node passed -> no zero nodes in list
            # this is the current time minus the time to get and open the node
            time_to_open_valve: int = travel_guide[me_starting_node][next_node] + 1
            # break if there is no more time
            if time_to_open_valve > me_minutes_left:
                continue
            # flow times the total amount valve can be open for
            possible_flow_released = valve_flows[next_node] * (me_minutes_left - time_to_open_valve)

            possible_flow_recursive = get_max_released_pressure_two_person(
                travel_guide=travel_guide, valve_flows=valve_flows,
                me_starting_node=next_node, elephant_starting_node=elephant_starting_node,
                me_minutes_left=me_minutes_left - time_to_open_valve, elephant_minutes_left=elephant_minutes_left,
                opened_valves=opened_valves + [next_node],  # this one is opened too recursively
            )

            if possible_flow_released + possible_flow_recursive > max_flow_value:
                max_flow_value = possible_flow_released + possible_flow_recursive
    else:
        # get next value for elephant
        # loop all non-zero keys
        for next_node in valve_flows.keys():
            # skip already opened valves / nodes
            if next_node in opened_valves:
                continue
            # skip zero nodes
            if valve_flows[next_node] == 0:
                continue

            # expect to open every node passed -> no zero nodes in list
            # this is the current time minus the time to get and open the node
            time_to_open_valve: int = travel_guide[elephant_starting_node][next_node] + 1
            # break if there is no more time
            if time_to_open_valve > elephant_minutes_left:
                continue
            # flow times the total amount valve can be open for
            possible_flow_released = valve_flows[next_node] * (elephant_minutes_left - time_to_open_valve)

            possible_flow_recursive = get_max_released_pressure_two_person(
                travel_guide=travel_guide, valve_flows=valve_flows,
                me_starting_node=me_starting_node, elephant_starting_node=next_node,
                me_minutes_left=me_minutes_left, elephant_minutes_left=elephant_minutes_left - time_to_open_valve,
                opened_valves=opened_valves + [next_node],  # this one is opened too recursively
            )

            if possible_flow_released + possible_flow_recursive > max_flow_value:
                max_flow_value = possible_flow_released + possible_flow_recursive

    return max_flow_value



class Test2022Day16(unittest.TestCase):
    test_tunnel, test_flow, test_non_zero_flow, test_edges, test_trave_guide = load_data("data/16-test.txt")

    def test_get_max_released_pressure(self):
        self.assertEqual(get_max_released_pressure(self.test_trave_guide, self.test_non_zero_flow), 1651)

    def test_get_max_released_pressure_with_two_people(self):
        self.assertEqual(get_max_released_pressure_two_person(self.test_trave_guide, self.test_non_zero_flow), 1707)


if __name__ == '__main__':
    print(">>> Start Main 16:")
    puzzle_tunnel, puzzle_flow, puzzle_non_zero_flow, puzzle_edges, puzzle_trave_guide = load_data("data/16.txt")
    print("Part 1): ", get_max_released_pressure(puzzle_trave_guide, puzzle_non_zero_flow))
    print("Part 2): ", get_max_released_pressure_two_person(puzzle_trave_guide, puzzle_non_zero_flow))
    print("End Main 16<<<")
