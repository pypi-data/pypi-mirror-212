"""
Tests for the ckk algorithm.
"""

# pylint: disable=missing-function-docstring, import-error

import pytest
from common import cmp_partition
from src import partitionpy

def test_too_few_numbers():
    with pytest.raises(ValueError):
        partitionpy.complete_karmarkar_karp([])
    with pytest.raises(ValueError):
        partitionpy.complete_karmarkar_karp([0])

def test_numbers():
    expected = ([8, 7], [6, 5, 4])
    actual = partitionpy.complete_karmarkar_karp([4,5,6,7,8])
    cmp_partition(expected, actual)

    expected = ([78], [6, 45, 8])
    actual = partitionpy.complete_karmarkar_karp([6,45,78,8])
    cmp_partition(expected, actual)

def test_indices_sorted():
    # kk does not sort internally, still check that the indices are still correct
    expected =([0, 1], [2, 3, 4])
    actual = partitionpy.complete_karmarkar_karp([8,7,6,5,4], return_indices=True)
    cmp_partition(expected, actual)

def test_indices_unsorted():
    # kk does not sort internally, still check that the indices are still correct
    expected =([4, 3], [2, 1, 0])
    actual = partitionpy.complete_karmarkar_karp([4,5,6,7,8], return_indices=True)
    cmp_partition(expected, actual)
