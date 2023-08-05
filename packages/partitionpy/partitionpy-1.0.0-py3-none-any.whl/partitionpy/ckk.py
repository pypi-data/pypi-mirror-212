"""
Complete karmarkar-karp algorithm
"""

from .types import Instance, Partition
from .complete_base import _complete_base
from .kk import karmarkar_karp

def complete_karmarkar_karp(instance: Instance, return_indices: bool=False) -> Partition:
    """
    Complete Karmarkar-Karp algorithm. Returns an optimal partition.
    Exponential runtime complexity. For more details see _complete_base

    :param: numbers is a list of integers.
    :param: return_indices can be set to true when the algorithm shall return the indices to build
            the partition instead of the partition itself

    Reference:
    R. E. Korf. A complete anytime algorithm for number partitioning. Artif. Intell., 106
      (2):181–203, dec 1998. ISSN 0004-3702. doi: 10.1016/S0004-3702(98)00086-1. URL
      https://doi.org/10.1016/S0004-3702(98)00086-1

    """
    return _complete_base(instance, return_indices, karmarkar_karp)
