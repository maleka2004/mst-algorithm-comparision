# -------------------------------------------------
# Local tests for Task A — the adjacency list.
# Run with: python -m tests.task_a
#
# NOT EXHAUSTIVE: the marking suite checks many more cases,
# including awkward ones these tests deliberately leave out.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from tests._helpers import check, banner, summary
from graph.adjacency_list import AdjacencyList
from graph.vertex import Vertex

banner("Task A (adjacency list)")

# The small network from Figure 4 of the specification:
#   Entrance --2-- d7,  Entrance --5-- d12,
#   d7 --3-- Power,     d12 --4-- Power
g = AdjacencyList()
ent = Vertex(0, "Entrance")
d7 = Vertex(1, "d7")
d12 = Vertex(2, "d12")
pwr = Vertex(3, "Power")
for v in (ent, d7, d12, pwr):
    g.add_vertex(v)

check(g.add_edge(ent, d7, 2), "add_edge Entrance--d7 returns True")
check(g.add_edge(ent, d12, 5), "add_edge Entrance--d12 returns True")
check(g.add_edge(d7, pwr, 3), "add_edge d7--Power returns True")
check(g.add_edge(d12, pwr, 4), "add_edge d12--Power returns True")

# ---- return types --------------------------------------------
check(isinstance(g.add_edge(ent, d7, 9), bool),
      "add_edge returns a bool")
check(isinstance(g.get_neighbours(ent), list),
      "get_neighbours returns a list")
nb = g.get_neighbours(pwr)
check(all(isinstance(t, tuple) and len(t) == 2 for t in nb),
      "get_neighbours items are (vertex, weight) tuples")
check(isinstance(g.get_edge_weight(ent, d7), int),
      "get_edge_weight returns an int")
check(isinstance(g.has_edge(ent, d7), bool),
      "has_edge returns a bool")
check(isinstance(g.get_edges(), list),
      "get_edges returns a list")
check(isinstance(g.num_edges(), int) and isinstance(g.num_vertices(), int),
      "num_edges and num_vertices return ints")

check(g.num_vertices() == 4, "num_vertices is 4")
check(g.num_edges() == 4, "num_edges is 4")
check(g.get_edge_weight(ent, d7) == 2, "get_edge_weight Entrance--d7 is 2")
check(g.get_edge_weight(d7, ent) == 2,
      "get_edge_weight is the same in both directions")
check(g.get_edge_weight(ent, pwr) == 0,
      "get_edge_weight is 0 for a missing connection")
check(g.has_edge(d12, pwr), "has_edge d12--Power is True")
check(not g.has_edge(d7, d12), "has_edge d7--d12 is False")

nbrs = sorted((n.name, w) for n, w in g.get_neighbours(pwr))
check(nbrs == [("d12", 4), ("d7", 3)],
      "get_neighbours Power lists d7 and d12 with the right firewalls")

check(g.update_edge_weight(ent, d7, 6), "update_edge_weight returns True")
check(g.get_edge_weight(d7, ent) == 6,
      "updated weight visible from both directions")

check(g.remove_edge(ent, d12), "remove_edge Entrance--d12 returns True")
check(g.num_edges() == 3, "num_edges falls to 3 after the removal")
check(g.get_edge_weight(ent, d12) == 0, "removed connection now reads 0")
check(len(g.get_edges()) == 3, "get_edges lists each connection once")

summary()
