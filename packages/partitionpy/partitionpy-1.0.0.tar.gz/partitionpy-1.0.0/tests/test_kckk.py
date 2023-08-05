"""
Tests for the kckk algorithm.
"""

# pylint: disable=missing-function-docstring, import-error

import pytest
from common import cmp_partition
from src import partitionpy

def test_too_few_numbers():
    with pytest.raises(ValueError):
        partitionpy.kernelized_complete_karmarkar_karp ([])
    with pytest.raises(ValueError):
        partitionpy.complete_karmarkar_karp([0])

def test_numbers():
    expected = ([8, 7], [6, 5, 4])
    actual = partitionpy.kernelized_complete_karmarkar_karp([4,5,6,7,8])
    cmp_partition(expected, actual)
