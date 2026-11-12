# -------------------------------------------------
# Local tests for Task B — Kruskal's algorithm.
# Run with: python -m tests.task_b
#
# NOT EXHAUSTIVE: the marking suite checks many more networks,
# including awkward ones these tests deliberately leave out.
#
# These tests build their network with the PROVIDED adjacency matrix,
# so they work whether or not you have finished Task A.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from tests._helpers import check, warn, banner, summary
from graph.adjacency_matrix import AdjacencyMatrix
from graph.vertex import Vertex
from mst.kruskals import kruskals
from mst.prims import prims

banner("Task B (Kruskal's algorithm)")

# The dense network from Figure 5 of the specification.
# Its minimum spanning tree disables 14 firewalls in total.
g = AdjacencyMatrix()
names = ["E", "d1", "d2", "d3", "R", "P"]
vs = {n: Vertex(i, n) for i, n in enumerate(names)}
for v in vs.values():
    g.add_vertex(v)
for a, b, f in [("E", "d1", 4), ("E", "P", 2), ("d1", "d2", 3),
                ("d2", "d3", 4), ("d3", "R", 2), ("R", "P", 5),
                ("E", "R", 3), ("d1", "d3", 8), ("E", "d2", 7),
                ("P", "d3", 9), ("d2", "R", 6)]:
    g.add_edge(vs[a], vs[b], f)

n_vertices = g.num_vertices()
prim_total = prims(g)[1]

tree, total = kruskals(g)

check(isinstance(tree, list), "kruskals returns (list, int): first is a list")
check(isinstance(total, int), "kruskals returns (list, int): second is an int")

# A spanning tree of a connected |V|-vertex graph has exactly |V|-1
# connections. Anything less is not a spanning tree (an empty return
# fails here, rather than slipping through).
check(len(tree) == n_vertices - 1,
      f"tree holds |V|-1 = {n_vertices - 1} connections (got {len(tree)})")
check(total == 14, f"total firewalls is 14 (got {total})")

# Guard against a vacuous pass: only meaningful once a tree is returned.
if tree:
    check(all(g.has_edge(e.u, e.v) for e in tree),
          "every chosen connection exists in the network")
    check(total == sum(e.weight for e in tree),
          "reported total equals the sum of the chosen connections")
else:
    warn("no tree returned yet, so per-connection checks are skipped")

check(total == prim_total and len(tree) == n_vertices - 1,
      f"total matches the provided Prim's ({prim_total})")

summary()
