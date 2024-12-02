"""
Implement basic mathematical operations on tuples, fully typed and tested.
"""

import math
from typing import Tuple, TypeVar, Union

Number = Union[int, float]
BaseVector = Tuple[Number, ...]
BaseVectorLength = TypeVar("BaseVectorLength", bound=BaseVector)


def tuple_add_tuple(a: BaseVectorLength, b: BaseVectorLength) -> BaseVectorLength:
    """sum of two tuples"""
    if len(a) != len(b):
        raise ValueError(f"Tuples should have same length. {len(a)} != {len(b)}")
    return tuple(map(lambda i, j: i + j, a, b))


def tuple_subtract_tuple(a: BaseVectorLength, b: BaseVectorLength) -> BaseVectorLength:
    """difference of first minus second tuple"""
    if len(a) != len(b):
        raise ValueError(f"Tuples should have same length. {len(a)} != {len(b)}")
    return tuple(map(lambda i, j: i - j, a, b))


def tuple_add_scalar(a: BaseVectorLength, b: Number) -> BaseVectorLength:
    """add constant to every val of tuple"""
    return tuple(map(lambda i: i + b, a))


def tuple_dot_tuple(a: BaseVectorLength, b: BaseVectorLength) -> Number:
    """scalar product between two equal length tuples"""
    if len(a) != len(b):
        raise ValueError(f"Tuples should have same length. {len(a)} != {len(b)}")
    return sum(map(lambda i, j: i * j, a, b))


def tuple_mult_tuple(a: BaseVectorLength, b: BaseVectorLength) -> BaseVectorLength:
    """multiply values of two equal length tuples"""
    if len(a) != len(b):
        raise ValueError(f"Tuples should have same length. {len(a)} != {len(b)}")
    return tuple(map(lambda i, j: i * j, a, b))


def tuple_mult_scalar(a: BaseVectorLength, b: Number) -> BaseVectorLength:
    """multiply every value of tuple with scalar"""
    return tuple(map(lambda i: i * b, a))


def tuple_mod_number(a: BaseVectorLength, b: Number) -> BaseVectorLength:
    """modulo of every value in tuple"""
    return tuple(map(lambda i: i % b, a))


def euclidean_distance(a: BaseVectorLength, b: BaseVectorLength) -> float:
    """calculate euclidean distance between two points"""
    if len(a) != len(b):
        raise ValueError(f"Tuples should have same length. {len(a)} != {len(b)}")
    return math.sqrt(sum((b[i] - a[i]) ** 2 for i in range(len(a))))


def manhattan_distance(a: BaseVectorLength, b: BaseVectorLength) -> Number:
    """given two positions calculate the manhattan distance"""
    if len(a) != len(b):
        raise ValueError(f"Tuples should have same length. {len(a)} != {len(b)}")
    return sum(map(lambda i, j: abs(i - j), a, b))


def tuple_euclidean_norm(a: BaseVector) -> float:
    """calculate euclidean norm of vector"""
    return math.sqrt(sum(value**2 for value in a))
