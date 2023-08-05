"""
Tests for the kk algorithm.
"""

# pylint: disable=missing-function-docstring, import-error

import pytest
from common import cmp_partition
from src import partitionpy

def test_too_few_numbers():
    with pytest.raises(ValueError):
        partitionpy.karmarkar_karp([])
    with pytest.raises(ValueError):
        partitionpy.karmarkar_karp([0])

def test_numbers():
    expected = ([8, 6], [7, 5, 4])
    actual = partitionpy.karmarkar_karp([4,5,6,7,8])
    cmp_partition(expected, actual)

def test_indices_sorted():
    # kk does not sort internally, still check that the indices are still correct
    expected =([1, 3, 4], [0, 2])
    actual = partitionpy.karmarkar_karp([8,7,6,5,4], return_indices=True)
    cmp_partition(expected, actual)

def test_indices_unsorted():
    # kk does not sort internally, still check that the indices are still correct
    expected =([0, 1, 3], [2, 4])
    actual = partitionpy.karmarkar_karp([4,5,6,7,8], return_indices=True)
    cmp_partition(expected, actual)
