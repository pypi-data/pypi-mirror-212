"""
Tests for the naive greedy algorithm.
"""

# pylint: disable=missing-function-docstring, import-error

import pytest
from common import cmp_partition
from src import partitionpy

def test_too_few_numbers():
    with pytest.raises(ValueError):
        partitionpy.naive_greedy([])
    with pytest.raises(ValueError):
        partitionpy.naive_greedy([0])

def test_numbers():
    expected = ([8, 5, 4], [7, 6])
    actual = partitionpy.naive_greedy([4,5,6,7,8])
    cmp_partition(expected, actual)

def test_indices_sorted():
    # greedy will sort internally, check that the indices are still correct
    expected =([4, 3, 0], [1, 2])
    actual = partitionpy.naive_greedy([8,7,6,5,4], return_indices=True)
    cmp_partition(expected, actual)

def test_indices_unsorted():
    # greedy will sort internally, check that the indices are still correct
    expected =([0, 1, 4], [2, 3])
    actual = partitionpy.naive_greedy([4,5,6,7,8], return_indices=True)
    cmp_partition(expected, actual)
