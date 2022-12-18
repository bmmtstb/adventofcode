import unittest
from copy import deepcopy
from typing import Dict, List, Tuple, Set, Union
import ast

from helper.file import load_file_and_split

Packet = List[Union[int, "Packet"]]  # every list contains zero or more comma-separated values
PacketPair = Tuple[Packet, Packet]
Packets = List[PacketPair]
OrderedPackets = List[Packet]


def load_packets(filepath: str) -> Packets:
    """load packets from file"""
    packets_raw = load_file_and_split(filepath=filepath, separator="\n\n")
    packets = []
    for packet_raw in packets_raw:
        left, right = packet_raw.split("\n")
        packets.append((ast.literal_eval(left), ast.literal_eval(right)))
    return packets


def is_correctly_sorted(pair: PacketPair) -> Union[bool, None]:
    """check whether a pair of packets is correctly sorted"""
    # When comparing two values, the first value is called left and the second value is called right. Then:
    left, right = pair
    # 1. If both values are integers, the lower integer should come first.
    if type(left) is int and type(right) is int:
        if left < right:
            # If the left integer is lower than the right integer, the inputs are in the right order.
            return True
        elif left > right:
            # If the left integer is higher than the right integer, the inputs are not in the right order.
            return False
        # Otherwise, the inputs are the same integer; continue checking the next part of the input.
        return None
    # 2. If both values are lists, compare the first value of each list, then the second value, and so on.
    elif type(left) is list and type(right) is list:
        for i in range(max(len(left), len(right))):
            if i >= len(left):
                # If the left list runs out of items first, the inputs are in the right order.
                return True
            elif i >= len(right):
                # If the right list runs out of items first, the inputs are not in the right order.
                return False
            else:
                # If the lists are the same length and no comparison makes a decision about the order,
                # continue checking the next part of the input.
                sub_sorted = is_correctly_sorted((left[i], right[i]))
                if sub_sorted is not None:
                    return sub_sorted
    # 3. If exactly one value is an integer, convert the integer to a list which contains that integer as its only
    # value, then retry the comparison.
    elif type(left) is int and type(right) is list:
        return is_correctly_sorted(([left], right))
    elif type(left) is list and type(right) is int:
        return is_correctly_sorted((left, [right]))
    else:
        raise NotImplementedError("should not reach this")


def sum_of_correct_packets(packets: Packets) -> int:
    """sum of correct sorted indices"""
    results = [is_correctly_sorted(pair) for pair in packets]
    return sum(index if result else 0 for index, result in enumerate(results, start=1))


def put_packets_in_correct_order(pair_packets: Packets) -> Tuple[OrderedPackets, int]:
    """put all packets in the right order, no more pairs"""
    # add divider packets and save them to find their indexes later
    divider1 = [[2]]
    divider2 = [[6]]
    all_packets: OrderedPackets = [divider1, divider2]
    for packet_pair in pair_packets:
        left, right = packet_pair
        all_packets.append(left)
        all_packets.append(right)
    # packets are now all in one big list
    ordered_packets = []
    for unordered_packet in all_packets:
        inserted = False
        # ordered list is empty
        if len(ordered_packets) == 0:
            ordered_packets.append(unordered_packet)
            continue
        for ordered_index, ordered_packet in enumerate(ordered_packets):
            # if not correctly sorted, unordered has to be before ordered, else check the next item
            if not is_correctly_sorted((ordered_packet, unordered_packet)):
                ordered_packets.insert(ordered_index, unordered_packet)
                inserted = True
                break
        # packet has not been inserted and therefore has to be at the end
        if not inserted:
            ordered_packets.append(unordered_packet)

    return ordered_packets, (ordered_packets.index(divider1) + 1) * (ordered_packets.index(divider2) + 1)


class Test2022Day13(unittest.TestCase):
    test_packets: Packets = load_packets("data/13-test.txt")
    test_result_order: OrderedPackets = [
        [],
        [[]],
        [[[]]],
        [1, 1, 3, 1, 1],
        [1, 1, 5, 1, 1],
        [[1], [2, 3, 4]],
        [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
        [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
        [[1], 4],
        [[2]],
        [3],
        [[4, 4], 4, 4],
        [[4, 4], 4, 4, 4],
        [[6]],
        [7, 7, 7],
        [7, 7, 7, 7],
        [[8, 7, 6]],
        [9]
    ]

    def test_predefined_examples(self):
        for pair_id, correctly_sorted in [
            (1, True),
            (2, True),
            (3, False),
            (4, True),
            (5, False),
            (6, True),
            (7, False),
            (8, False),
        ]:
            with self.subTest(msg=f'Pair: {self.test_packets[pair_id - 1]}, should_be_correct: {correctly_sorted}'):
                self.assertEqual(is_correctly_sorted(deepcopy(self.test_packets)[pair_id - 1]), correctly_sorted)

    def test_sum_of_correct_packets(self):
        self.assertEqual(sum_of_correct_packets(deepcopy(self.test_packets)), 13)

    def test_put_packets_in_correct_order(self):
        result_packets, decoder_key = put_packets_in_correct_order(deepcopy(self.test_packets))
        self.assertListEqual(result_packets, self.test_result_order)
        self.assertEqual(decoder_key, 140)


if __name__ == '__main__':
    print(">>> Start Main 13:")
    puzzle_input: Packets = load_packets("data/13.txt")
    print("Part 1): ", sum_of_correct_packets(puzzle_input))
    print("Part 2): ", put_packets_in_correct_order(puzzle_input)[1])
    print("End Main 13<<<")
