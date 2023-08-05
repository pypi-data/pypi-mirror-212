"""
Common test helpers
"""

def cmp_partition(expected, actual):
    """
    Compares two partitions for equivalence.
    """
    exp_a, exp_b = expected
    act_a, act_b = actual

    # the order of the numbers in the output is undefined, therefore sort
    exp_a.sort()
    exp_b.sort()
    act_a.sort()
    act_b.sort()

    # which list is a anb b is undefined
    if exp_a == act_a:
        assert exp_b ==  act_b
    else:
        assert exp_a ==  act_b
        assert exp_b ==  act_a
