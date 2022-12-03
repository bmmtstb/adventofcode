import math
from typing import Tuple, Union

Number = Union[int, float]
BaseVector = Tuple[Number, ...]


def tuple_add_tuple(a: BaseVector, b: BaseVector) -> BaseVector:
    """sum of two tuples"""
    if len(a) != len(b):
        raise ValueError("Tuples should have same length. {} != {}".format(len(a), len(b)))
    return tuple(map(lambda i, j: i + j, a, b))


def tuple_subtract_tuple(a: BaseVector, b: BaseVector) -> BaseVector:
    """difference of first minus second tuple"""
    if len(a) != len(b):
        raise ValueError("Tuples should have same length. {} != {}".format(len(a), len(b)))
    return tuple(map(lambda i, j: i - j, a, b))


def tuple_add_scalar(a: BaseVector, b: Number) -> BaseVector:
    """add constant to every val of tuple"""
    return tuple(map(lambda i: i + b, a))


def tuple_dot_tuple(a: BaseVector, b: BaseVector) -> Number:
    """scalar product between two equal length tuples"""
    if len(a) != len(b):
        raise ValueError("Tuples should have same length. {} != {}".format(len(a), len(b)))
    return sum(map(lambda i, j: i * j, a, b))


def tuple_mult_tuple(a: BaseVector, b: BaseVector) -> BaseVector:
    """multiply values of two equal length tuples"""
    if len(a) != len(b):
        raise ValueError("Tuples should have same length. {} != {}".format(len(a), len(b)))
    return tuple(map(lambda i, j: i * j, a, b))


def tuple_mult_scalar(a: BaseVector, b: Number) -> BaseVector:
    """multiply every value of tuple with scalar"""
    return tuple(map(lambda i: i * b, a))


def tuple_mod_number(a: BaseVector, b: Number) -> BaseVector:
    """modulo of every value in tuple"""
    return tuple(map(lambda i: i % b, a))


def euclidean_distance(a: BaseVector, b: BaseVector) -> float:
    """calculate euclidean distance between two points"""
    if len(a) != len(b):
        raise ValueError("Tuples should have same length. {} != {}".format(len(a), len(b)))
    return math.sqrt(sum((b[i] - a[i]) ** 2 for i in range(len(a))))


def tuple_euclidean_norm(a: BaseVector) -> float:
    """calculate euclidean norm of vector"""
    return math.sqrt(sum(value ** 2 for value in a))

