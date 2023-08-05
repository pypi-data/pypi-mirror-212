"""
Simplest naive greedy algorithm.
"""
from typing import List
from .types import Instance, Partition

def naive_greedy(numbers_unsorted: Instance, return_indices: bool=False) -> Partition:
    """
    Probably the simplest greedy algorithm for partitioning.

    Runtime complexity in O(n) and generally fast.
    Yields discrepancy in O(1/n) on average.

    :param: numbers is a list of integers.
    :param: return_indices can be set to true when the algorithm shall return the indices to build
            the partition instead of the partition itself
    """
    if len(numbers_unsorted) < 2:
        raise ValueError("PARTITION instance must contain at least 2 numbers")

    numbers, indices = zip(*sorted(
            zip(numbers_unsorted, range(len(numbers_unsorted))), reverse=True))

    list_a = []  # type: List[int]
    list_b = []  # type: List[int]
    sum_a = 0
    sum_b = 0

    for idx, number in zip(indices, numbers):
        if sum_a <= sum_b:
            list_a.append(idx if return_indices else number)
            sum_a += number
        else:
            list_b.append(idx if return_indices else number)
            sum_b += number

    return (list_a, list_b)
