import unittest
from typing import Dict, List, Tuple, Set

from helper.file import read_lines_as_list


def load(fp: str) -> List[int]:
    return read_lines_as_list(fp, instance_type=int)


class Node:
    def __init__(self, value, id_):
        self.value: int = value
        self.id: int = id_
        self.prev: Node = None
        self.next: Node = None

    def link(self, prev_: "Node", next_: "Node"):
        self.prev: Node = prev_
        self.next: Node = next_


class LinkedList:
    def __init__(self, fp: str):
        data = load(fp)
        self.zero_id = data.index(0)

        # init nodes
        self.state: Tuple[Node] = tuple(
            [Node(value, i) for i, value in enumerate(data)]
        )
        # then link them
        for i, n in enumerate(self.state):
            n.link(self.state[i - 1], self.state[(i + 1) % len(data)])

    def get_score(self) -> int:
        """1000th, 2000th and 3000th value after 0"""

        a = self.nth(1000, self.state[self.zero_id])
        b = self.nth(1000, a)
        c = self.nth(1000, b)
        return a.value + b.value + c.value

    def visualize(self, idx: int = 0) -> List[int]:
        l = []
        curr_node = self.state[idx]
        start_id = curr_node.id
        l.append(curr_node.value)
        curr_node = curr_node.next
        while curr_node.id != start_id:
            l.append(curr_node.value)
            curr_node = curr_node.next
        print(l)
        return l

    @staticmethod
    def nth(n: int, node: Node) -> Node:
        if n == 0:
            return node

        new_node = node
        for _ in range(abs(n)):
            new_node = new_node.next if n >= 0 else new_node.prev
        return new_node

    @staticmethod
    def remove(node: Node) -> None:
        prev_node = node.prev
        next_node = node.next
        # change prev
        prev_node.next = next_node
        # change next
        next_node.prev = prev_node
        # change self
        node.next = node
        node.prev = node

    @staticmethod
    def insert_after(loc_node: Node, new_node: Node) -> None:
        next_node = loc_node.next
        # loc -> new_idx
        loc_node.next = new_node
        new_node.prev = loc_node
        # new_idx -> loc.next()
        new_node.next = next_node
        next_node.prev = new_node

    @staticmethod
    def insert_before(loc_node: Node, new_node: Node) -> None:
        next_node = loc_node.prev
        # loc -> new_idx
        loc_node.prev = new_node
        new_node.next = loc_node
        # new_idx -> loc.next()
        new_node.prev = next_node
        next_node.next = new_node

    def move_node(self, idx: int) -> None:
        curr_node: Node = self.state[idx]
        # trivial case no change
        if curr_node.value == 0:
            return

        nth_node = self.nth(curr_node.value, curr_node)

        # cut current node from graph
        self.remove(curr_node)

        if curr_node.value > 0:
            self.insert_after(nth_node, curr_node)
        else:
            self.insert_before(nth_node, curr_node)

    def decrypt(self) -> int:
        for i in range(len(self.state)):
            self.move_node(i)
        return self.get_score()


class Test2022Day20(unittest.TestCase):

    def test_get_result(self):
        self.assertEqual(LinkedList("./data/20-test.txt").decrypt(), 3)


if __name__ == "__main__":
    print(">>> Start Main 20:")
    puzzle_input = LinkedList("./data/20.txt")
    print("Part 1): ", puzzle_input.decrypt())  # 2622
    print("Part 2): ", ...)  # 1538773034088
    print("End Main 20<<<")
