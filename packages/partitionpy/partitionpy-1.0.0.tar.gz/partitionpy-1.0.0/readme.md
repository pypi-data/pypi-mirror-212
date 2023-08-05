# partition package

This is a collection of several algorithms to solve [PARTITION](https://en.wikipedia.org/wiki/Partition_problem).

![test](https://github.com/llueder/partitionpy/actions/workflows/python-app.yml/badge.svg) ![lint](https://github.com/llueder/partitionpy/actions/workflows/pylint.yml/badge.svg) ![mypy](https://github.com/llueder/partitionpy/actions/workflows/mypy.yml/badge.svg) [![coverage](https://llueder.github.io/partitionpy/badges/coverage.svg)](https://github.com/llueder/partitionpy/actions)

The package offers two heuristics:
* the [naive greedy heuristic](https://github.com/llueder/partitionpy/tree/main/src/partitionpy/naive_greedy.py)
* the [Karmakar-Karp heuristic](https://github.com/llueder/partitionpy/tree/main/src/partitionpy/kk.py) or Largest Differencing Method (LDM)
and a complete algorithm,
* the [Complete Karmarkar-Karp algorithm](https://github.com/llueder/partitionpy/tree/main/src/partitionpy/ckk.py).

The latter is also available in a more efficient [version](https://github.com/llueder/partitionpy/tree/main/src/partitionpy/kckk.py) for some instances.

## Resources on the partition problem

The implementation stem from a project during my master's degree.
The resulting thesis is [available](https://github.com/llueder/partitionpy/tree/main/doc/partition_llueder.pdf), feel free to read especially the sections 1 to 3.
From the references, I would like to recommend the following publications in particular:

R. E. Korf. A complete anytime algorithm for number partitioning. Artif. Intell., 106(2):
181–203, dec 1998. ISSN 0004-3702. [doi:10.1016/S0004-3702(98)00086-1](https://doi.org/10.1016/S0004-3702(98)00086-1).

B. Hayes. Computing science: The easiest hard problem. American Scientist, 90(2):113–117,
2002. ISSN 00030996. URL [http://www.jstor.org/stable/27857621](http://www.jstor.org/stable/27857621).

S. Mertens. The easiest hard problem: number partitioning. In Computational
Complexity and Statistical Physics. Oxford University Press, 12 2005. ISBN 9780195177374.
[doi:10.1093/oso/9780195177374.003.0012](https://doi.org/10.1093/oso/9780195177374.003.0012).

## Installation and usage

Run `pip install partitionpy` to install.

Example code:
```
import partitionpy

partitionpy.karmarkar_karp([4,5,6,7,8])
partitionpy.naive_greedy([4,5,6,7,8])
partitionpy.complete_karmarkar_karp([4,5,6,7,8])
partitionpy.kernelized_complete_karmarkar_karp([4,5,6,7,8])
partitionpy.complete_greedy([4,5,6,7,8])
```

## Alternatives

This is by far not the only package for PARTITION. You may want to check out [numberpartitioning](https://pypi.org/project/numberpartitioning/) and [prtpy](https://pypi.org/project/prtpy/) as well.
