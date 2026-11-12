# -------------------------------------------------
# DO NOT CHANGE THIS FILE.
# Prim's algorithm, provided as the reference MST solver.
# In your report (B.1) you will read this implementation and
# write pseudo-code for it.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from graph.graph import Graph
from mst.min_heap import MinHeap
from graph.vertex import Vertex
from graph.edge import Edge


def prims(graph: Graph) -> tuple[list[Edge], int]:
    """
    Computes a minimum spanning tree of a connected graph using Prim's
    algorithm with the provided indexed binary min-heap (mst/min_heap.py).

    The algorithm grows a single tree from a starting vertex. Every
    vertex not yet in the tree sits in the priority queue at most once,
    keyed on the lightest known connection reaching it. Each step removes
    the closest such vertex, adds its connection to the tree, and then
    relaxes its neighbours: if a neighbour can now be reached more
    cheaply, its priority is lowered in place (decrease-key).

    @param graph: The graph to span. Must be connected.
    @returns: A tuple of:
              - list[Edge]: the connections chosen for the tree.
              - int: the total number of firewalls across the tree.
    """
    vertices = graph.get_vertices()
    if not vertices:
        return [], 0

    # Every vertex starts in the queue with infinite priority and no
    # parent; the start vertex is given priority 0 so it is popped first.
    INF = float("inf")
    queue = MinHeap()
    start = vertices[0]
    queue.push(0, start, None)
    for v in vertices:
        if v != start:
            queue.push(INF, v, None)

    in_tree: set[Vertex] = set()
    tree: list[Edge] = []
    total = 0

    while len(queue) > 0:
        weight, v, parent = queue.pop()
        in_tree.add(v)
        if parent is not None:
            tree.append(Edge(parent, v, weight))
            total += weight
        for neighbour, w in graph.get_neighbours(v):
            if neighbour not in in_tree and neighbour in queue:
                queue.decrease_key(neighbour, w, v)

    return tree, total
