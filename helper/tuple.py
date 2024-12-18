"""
Implement basic mathematical operations on tuples, fully typed and tested.
"""

import math
from typing import Tuple, TypeVar, Union

Number = Union[int, float]
BaseVector = Tuple[Number, ...]
BaseVectorLength = TypeVar("BaseVectorLength", bound=BaseVector)


def tuple_add_tuple(a: BaseVectorLength, b: BaseVectorLength) -> BaseVectorLength:
    """Sum of two tuples.

    Raises:
        ValueError: If the tuples are not of the same length.

    """
    if len(a) != len(b):
        raise ValueError(f"Tuples should have same length. {len(a)} != {len(b)}")
    if len(a) == 0:
        raise ValueError("Tuples should not be empty.")
    return tuple(map(lambda i, j: i + j, a, b))


def tuple_subtract_tuple(a: BaseVectorLength, b: BaseVectorLength) -> BaseVectorLength:
    """Difference of first minus second tuple.

    Raises:
        ValueError: If the tuples are not of the same length.
    """
    if len(a) != len(b):
        raise ValueError(f"Tuples should have same length. {len(a)} != {len(b)}")
    if len(a) == 0:
        raise ValueError("Tuples should not be empty.")
    return tuple(map(lambda i, j: i - j, a, b))


def tuple_add_scalar(a: BaseVectorLength, b: Number) -> BaseVectorLength:
    """Add a constant to every val of tuple"""
    if len(a) == 0:
        raise ValueError("Tuple a should not be empty.")
    return tuple(map(lambda i: i + b, a))


def tuple_dot_tuple(a: BaseVectorLength, b: BaseVectorLength) -> Number:
    """Compute the scalar product between two equal length tuples.

    Raises:
        ValueError: If the tuples are not of the same length.
    """
    if len(a) != len(b):
        raise ValueError(f"Tuples should have same length. {len(a)} != {len(b)}")
    if len(a) == 0:
        raise ValueError("Tuples should not be empty.")
    return sum(map(lambda i, j: i * j, a, b))


def tuple_mult_tuple(a: BaseVectorLength, b: BaseVectorLength) -> BaseVectorLength:
    """Multiply values of two equal length tuples.

    Raises:
        ValueError: If the tuples are not of the same length.
    """
    if len(a) != len(b):
        raise ValueError(f"Tuples should have same length. {len(a)} != {len(b)}")
    if len(a) == 0:
        raise ValueError("Tuples should not be empty.")
    return tuple(map(lambda i, j: i * j, a, b))


def tuple_mult_scalar(a: BaseVectorLength, b: Number) -> BaseVectorLength:
    """Multiply every value of tuple with scalar."""
    if len(a) == 0:
        raise ValueError("Tuple a should not be empty.")
    return tuple(map(lambda i: i * b, a))


def tuple_mod_number(a: BaseVectorLength, b: Number) -> BaseVectorLength:
    """Modulo of every value in tuple."""
    if len(a) == 0:
        raise ValueError("Tuple a should not be empty.")
    return tuple(map(lambda i: i % b, a))


def tuple_mod_tuple(a: BaseVectorLength, b: BaseVectorLength) -> BaseVectorLength:
    """Modulo of every value in tuple using the value of the other tuple."""
    if len(a) != len(b):
        raise ValueError(f"Tuples should have same length. {len(a)} != {len(b)}")
    if len(a) == 0:
        raise ValueError("Tuple a should not be empty.")
    return tuple(map(lambda i, j: i % j, a, b))


def euclidean_distance(a: BaseVectorLength, b: BaseVectorLength) -> float:
    """Calculate the Euclidean distance between two points.

    Raises:
        ValueError: If the tuples are not of the same length.
    """
    if len(a) != len(b):
        raise ValueError(f"Tuples should have same length. {len(a)} != {len(b)}")
    if len(a) == 0:
        raise ValueError("Tuples should not be empty.")
    return math.sqrt(sum((b[i] - a[i]) ** 2 for i in range(len(a))))


def manhattan_distance(a: BaseVectorLength, b: BaseVectorLength) -> Number:
    """Given two positions, calculate the manhattan distance.

    Raises:
        ValueError: If the tuples are not of the same length.
    """
    if len(a) != len(b):
        raise ValueError(f"Tuples should have same length. {len(a)} != {len(b)}")
    if len(a) == 0:
        raise ValueError("Tuples should not be empty.")
    return sum(map(lambda i, j: abs(i - j), a, b))


def tuple_euclidean_norm(a: BaseVector) -> float:
    """Calculate the Euclidean norm of a vector."""
    if len(a) == 0:
        raise ValueError("Tuple a should not be empty.")
    return math.sqrt(sum(value**2 for value in a))
