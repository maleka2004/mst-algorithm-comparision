# -------------------------------------------------
# DO NOT CHANGE THIS FILE.
# Brute-force freighter loader, provided as a naive baseline.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from fold.databrick import Databrick


def brute_force_load(bricks: list[Databrick],
                     weight_capacity: int,
                     volume_capacity: int | None = None
                     ) -> tuple[list[Databrick], int, int, int, None]:
    """
    Chooses which databricks to load by trying every possible
    combination and keeping the best valid one.

    A load is valid when its total weight fits within weight_capacity
    and, if volume_capacity is a number, its total volume fits within
    volume_capacity as well. Passing volume_capacity as None switches
    the volume limit off entirely.

    Among all valid loads that free the most records, the one with
    the smallest total weight is kept (a lighter freighter flies
    faster).

    WARNING: the number of combinations doubles with every extra
    databrick, so this loader is only usable for very small hauls.
    It exists as a correctness baseline for Task D.

    @param bricks: The recovered databricks to choose from.
    @param weight_capacity: The freighter's weight limit in kilograms.
    @param volume_capacity: The freighter's volume limit in litres,
                            or None for no volume limit.
    @returns: A tuple of:
              - list[Databrick]: the databricks to load.
              - int: total records freed.
              - int: total weight loaded.
              - int: total volume loaded.
              - None: placeholder where the freighter loader returns
                      its memo table, kept so both loaders share a
                      return shape.
    """
    n = len(bricks)
    best: tuple[int, int, int, list[Databrick]] = (0, 0, 0, [])

    for mask in range(1 << n):
        value = weight = volume = 0
        subset: list[Databrick] = []
        for i in range(n):
            if mask & (1 << i):
                b = bricks[i]
                value += b.records
                weight += b.weight
                volume += b.volume
                subset.append(b)
        if weight > weight_capacity:
            continue
        if volume_capacity is not None and volume > volume_capacity:
            continue
        if (value > best[0]
                or (value == best[0] and weight < best[1])):
            best = (value, weight, volume, subset)

    value, weight, volume, subset = best
    return subset, value, weight, volume, None
