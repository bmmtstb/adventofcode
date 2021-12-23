import math
from typing import Dict, List, Tuple, Set, Union

BaseVector = Tuple[int, ...]


def tuple_add_tuple(a: BaseVector, b: BaseVector) -> BaseVector:
    """sum of two tuples"""
    if len(a) != len(b):
        raise ValueError("Tuples should have same length. {} != {}".format(len(a), len(b)))
    return tuple(map(lambda i, j: i + j, a, b))


def tuple_add_scalar(a: BaseVector, b: Union[int, float]) -> BaseVector:
    """add constant to every val of tuple"""
    return tuple(map(lambda i: i + b, a))


def tuple_dot_tuple(a: BaseVector, b: BaseVector) -> Union[int, float]:
    """scalar product between two equal length tuples"""
    if len(a) != len(b):
        raise ValueError("Tuples should have same length. {} != {}".format(len(a), len(b)))
    return sum(map(lambda i, j: i * j, a, b))


def tuple_mult_tuple(a: BaseVector, b: BaseVector) -> BaseVector:
    """multiply values of two equal length tuples"""
    if len(a) != len(b):
        raise ValueError("Tuples should have same length. {} != {}".format(len(a), len(b)))
    return tuple(map(lambda i, j: i * j, a, b))


def tuple_mult_scalar(a: BaseVector, b: Union[int, float]) -> BaseVector:
    """multiply every value of tuple with scalar"""
    return tuple(map(lambda i: i * b, a))


def tuple_mod_number(a: BaseVector, b: Union[int, float]) -> BaseVector:
    """modulo of every value in tuple"""
    return tuple(map(lambda i: i % b, a))


def euclidean_distance(a: BaseVector, b: BaseVector) -> float:
    """calculate euclidean distance between two points"""
    if len(a) != len(b):
        raise ValueError("Tuples should have same length. {} != {}".format(len(a), len(b)))
    return math.sqrt(sum((b[i] - a[i]) ** 2 for i in range(len(a))))
