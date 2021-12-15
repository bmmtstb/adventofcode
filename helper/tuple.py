import math
from typing import Dict, List, Tuple, Set


def tuple_add_tuple(a: Tuple[int, ...], b: Tuple[int, ...]):
    """sum of two tuples"""
    if len(a) != len(b):
        raise ValueError("Tuples should have same length. {} != {}".format(len(a), len(b)))
    return tuple(map(lambda i, j: i + j, a, b))


def tuple_add_scalar(a: Tuple[int, ...], b: int):
    """add constant to every val of tuple"""
    return tuple(map(lambda i: i + b, a))


def tuple_mult_tuple(a: Tuple[int, ...], b: Tuple[int, ...]):
    """multiply values of two equal length tuples"""
    if len(a) != len(b):
        raise ValueError("Tuples should have same length. {} != {}".format(len(a), len(b)))
    return tuple(map(lambda i, j: i * j, a, b))


def tuple_mult_scalar(a: Tuple[int, ...], b: int):
    """multiply every value of tuple with scalar"""
    return tuple(map(lambda i: i * b, a))


def euclidean_distance(a: Tuple[int, ...], b: Tuple[int, ...]) -> float:
    """calculate euclidean distance between two points"""
    if len(a) != len(b):
        raise ValueError("Tuples should have same length. {} != {}".format(len(a), len(b)))
    return math.sqrt(sum((b[i] - a[i]) ** 2 for i in range(len(a))))
