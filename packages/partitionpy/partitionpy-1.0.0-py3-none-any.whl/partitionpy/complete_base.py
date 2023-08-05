"""
Base implementation for a complete algorithm following
R. E. Korf. A complete anytime algorithm for number partitioning. Artif. Intell., 106
      (2):181–203, dec 1998. ISSN 0004-3702. doi: 10.1016/S0004-3702(98)00086-1. URL
      https://doi.org/10.1016/S0004-3702(98)00086-1
"""

from typing import Callable, List, Tuple

from .types import Instance, Partition

def _complete_base(instance: Instance, return_indices: bool,
        heuristic: Callable[[Instance, bool], Partition]) -> Partition:
    """
    Base for complete algorithms. Takes a heuristic algorithm as a start.

    Stops when a perfect partition is found.
    If the current discrepancy is larger than the sum of remaining numbers, the only option is to
    put all of them in the smaller list.

    Open tasks:
    * implement Limited Discrepancy Search
    * make it a true anytime algorithm; implement possibility to stop manually before the algorithm
      has finished
    * the function is quite complex and pylint is not happy. Break it down better.
    """
    # pylint: disable=too-many-locals, too-many-branches
    if len(instance) < 2:
        raise ValueError("PARTITION instance must contain at least 2 numbers")

    numbers_, indices = zip(*sorted(
            zip(instance, range(len(instance))), reverse=True))
    numbers = [int(number) for number in numbers_]  # this line is just for mypy

    best_path = best_diff = None
    visited_nodes, visited_leafs = 0, 0
    tree_depth = len(numbers)
    direction = [0 for _ in numbers]  # type: List[int]

    heuristic_result = heuristic(numbers, True)

    # since the semantics of a branching decision is whether to use the KK
    # result or not, we have to store the KK decision for each number.
    for idx in heuristic_result[1]:
        direction[idx] = 1

    # A path is a sequence of decisions.
    # The main information is the decision itself, but for runtime efficiency,
    # we store the current sum as additional information, so that we don't have
    # to calculate it again every time.
    # It doesn't matter where the first number goes. The two subtrees have the same partitions,
    # just with list_a and list_b exchanged. But we should respect the KK decision for the
    # number, so that the directions are consistent
    #                   path   sums    sum of remaining
    paths_stack = []  # type: List[Tuple[List[int], List[int], int]]
    if direction[0] == 0:
        paths_stack = [([0],    [numbers[0], 0], sum(numbers) - numbers[0])]
    else:
        paths_stack = [([1],    [0, numbers[0]], sum(numbers) - numbers[0])]

    break_ctr = 0
    while paths_stack:
        path, sums, sum_remaining = paths_stack.pop()
        visited_nodes += 1

        level = len(path)
        if level != tree_depth:
            diff = abs(sums[0] - sums[1])
            # check whether we can prune
            if diff > sum_remaining:
                if best_diff is not None and diff - sum_remaining > best_diff:
                    continue  # no chance of getting better
                # put all numbers into the smaller set, this is the best option
                smaller_idx = 0 if sums[0] < sums[1] else 1
                new_path = path + [smaller_idx] * (tree_depth-level)
                sums[smaller_idx] += sum_remaining
                paths_stack.append((new_path, sums, 0))
            else:
                # put both options in a tuple to assign to left and
                # right branch according to the heuristic.
                paths = (path + [0], path + [1])
                sums_0 = [sums[0] + numbers[level], sums[1]]
                sums_1 = [sums[0], sums[1] + numbers[level]]
                paths_sums  = [sums_0, sums_1]

                sum_remaining -= numbers[level]
                paths_stack.append((paths[1-direction[level]], paths_sums[1-direction[level]],
                        sum_remaining))
                paths_stack.append((paths[  direction[level]], paths_sums[  direction[level]],
                        sum_remaining))
        else:
            # we are at a leaf
            visited_leafs += 1
            diff = abs(sums[1] - sums[0])
            if best_diff is None or diff < best_diff:
                best_diff, best_path = diff, path
            if best_diff <= 1.1:
                break_ctr += 1
                break

    assert best_path
    best_sets = ([], [])  # type: Partition
    for idx, decision in enumerate(best_path):
        best_sets[decision].append(indices[idx] if return_indices else numbers[idx])

    return best_sets
