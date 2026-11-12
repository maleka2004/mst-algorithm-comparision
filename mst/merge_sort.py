# -------------------------------------------------
# DO NOT CHANGE THIS FILE.
# Merge sort over edges, provided for Task B.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from graph.edge import Edge


def merge_sort(edges: list[Edge]) -> list[Edge]:
    """
    Returns a new list containing the given edges ordered by weight,
    lightest first. Edges of equal weight keep their original relative
    order. The input list is not modified.

    @param edges: The edges to sort.
    @returns: A new list of the same edges, ordered by weight ascending.
    """
    if len(edges) <= 1:
        return list(edges)
    mid = len(edges) // 2
    left = merge_sort(edges[:mid])
    right = merge_sort(edges[mid:])
    merged: list[Edge] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i].weight <= right[j].weight:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
