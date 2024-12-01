import unittest
from typing import Dict, List, Tuple, Set

special_value = 20201227


def transform_subject_number(sub_num: int, loop_size: int) -> int:
    """transform subject number"""
    val = 1
    for _ in range(loop_size):
        val *= sub_num
        val = val % special_value  # remainder
    return val


def get_loop_size(sub_num: int, pub_key: int) -> int:
    """find the loop size of a pub key"""
    n = 0
    val = 1
    while val != pub_key:
        val *= sub_num
        val = val % special_value  # remainder
        n += 1
    return n


def handshake(card_pub: int, door_pub: int) -> int:
    """perform cryptographic handshake"""
    card_sub_num = 7
    door_sub_num = 7
    # get device loop sizes
    card_loop_size = get_loop_size(card_sub_num, card_pub)
    door_loop_size = get_loop_size(door_sub_num, door_pub)
    # use loop sizes to calc private key
    encryption_key = transform_subject_number(door_pub, card_loop_size)
    encryption_key_v2 = transform_subject_number(card_pub, door_loop_size)
    if encryption_key != encryption_key_v2:
        raise Exception("Keys not equal")
    return encryption_key


class Test2020Day25(unittest.TestCase):

    def test_loop_size(self):
        for pub, num, n in [
            [5764801, 7, 8],
            [17807724, 7, 11],
        ]:
            with self.subTest():
                self.assertEqual(get_loop_size(num, pub), n)

    def test_handshake(self):
        self.assertEqual(handshake(card_pub=5764801, door_pub=17807724), 14897079)


if __name__ == "__main__":
    print(">>> Start Main 25:")
    puzzle_input = [13135480, 8821721]  # card and door pub key
    print("Part 1):")
    print(handshake(card_pub=puzzle_input[0], door_pub=puzzle_input[1]))
    print("Part 2):")
    print("Just click and you are done :)")
    print("End Main 25<<<")
