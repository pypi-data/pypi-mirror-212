"""
A kernelized version of CKK.
"""

from typing import Dict, List, Tuple

from .types import Instance, Partition
from .kk import karmarkar_karp

def kernelized_complete_karmarkar_karp(instance: Instance) -> Partition:
    """
    Kernelized version of CKK.

    Runtime complexity in O(n^k), where k is the number of different values in the input.

    References:
    See complete_karmarkar_karp for the basics. The kernelization has not been described before,
    as far as I am aware.

    The idea is very simple. Take an instance with n numbers with k different values with at most m
    bit resolution. For each value, it can be stored in O(m) bit. The number of occurrences can be
    stored in O(logn) bit for each value. So in total, the instance can be encoded in O(m)+
    can be encoded in O(k*m) bit. For each value denote the value in O(m) and number of ocurrences
    in O(log_2(n)).

    :param: instance is a list of integers.
    """
    # pylint: disable=too-many-locals, too-many-branches
    if len(instance) < 2:
        raise ValueError("PARTITION instance must contain at least 2 numbers")

    # run the Karmarkar-Karp heuristic to get a starting point
    heuristic_result = karmarkar_karp(instance, True)

    # since the semantics of a branching decision is whether to use the KK
    # result or not, we have to store the KK decision for each number.
    direction = [0 for _ in instance]
    for idx in heuristic_result[1]:
        direction[idx] = 1

    total_cnt = {}  # type: Dict[int, int]
    heuristic_cnt = {}  # type: Dict[int, int]
    for idx, num in enumerate(instance):
        total_cnt.setdefault(num, 0)
        heuristic_cnt.setdefault(num, 0)
        total_cnt[num] = total_cnt[num] + 1
        heuristic_cnt[num] = heuristic_cnt[num] + direction[idx]

    # A path is a sequence of decisions.
    # The main information is the decision itself, but for runtime efficiency,
    # we store the current sum as additional information, so that we don't have
    # to calculate it again every time.
    #               path   sums    sum of remaining
    paths_stack = [([],    [0, 0], sum(instance))]  # type: List[Tuple[List[int], List[int], int]]

    best_path = None
    best_diff = None
    visited_nodes = 0
    visited_leaves = 0

    numbers = list(total_cnt.keys())
    tree_depth = len(numbers)
    # pylint: disable=duplicate-code
    # there are decisive differences and without larger rewrite, I cannot remove the duplication
    while paths_stack:
        path, sums, sum_remaining = paths_stack.pop()
        visited_nodes += 1

        level = len(path)
        if level != tree_depth:
            diff = abs(sums[0] - sums[1])
            # check whether we can prune
            if diff > sum_remaining:
                if best_diff is not None and diff - sum_remaining > best_diff:
                    continue  # no change of getting better
                # put all numbers into the smaller set, this is the best option
                smaller_idx = 0 if sums[0] < sums[1] else 1
                new_path = path + [total_cnt[numbers[idx]]*(1-smaller_idx)
                        for idx in range(level, tree_depth)]
                sums[smaller_idx] += sum_remaining
                paths_stack.append((new_path, sums, 0))
            else:
                num = numbers[level]
                sum_remaining -= num*total_cnt[num]

                # We try out adding 0 left, 1 left etc. But we start with the heuristic number
                try_numbers = [(heuristic_cnt[num] + i) % (total_cnt[num] + 1)
                        for i in range(total_cnt[num] + 1)]
                paths = [path + [try_number] for try_number in try_numbers]
                sums_  = [[sums[0] + try_number*num, sums[1] + (total_cnt[num]-try_number)*num]
                        for try_number in try_numbers]

                for path_, sum_ in zip(reversed(paths), reversed(sums_)):
                    paths_stack.append((path_, sum_, sum_remaining))
        else:
            # we are at a leaf
            visited_leaves += 1
            assert sum_remaining == 0
            diff = abs(sums[1] - sums[0])
            if best_diff is None or diff < best_diff:
                best_diff, best_path = diff, path
            if best_diff <= 1.1:
                break

    assert best_path
    best_sets = ([], [])  # type: Partition
    for idx, decision in enumerate(best_path):
        for i in range(decision):
            best_sets[1].append(numbers[idx])
        for i in range(total_cnt[numbers[idx]] - decision):
            best_sets[0].append(numbers[idx])

    return best_sets
