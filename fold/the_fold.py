# -------------------------------------------------
# DO NOT CHANGE THIS FILE.
# Builds The Fold: the Monarch's data storage network.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

import random

from graph.graph import Graph
from graph.vertex import Vertex
from graph.adjacency_list import AdjacencyList
from graph.adjacency_matrix import AdjacencyMatrix
from fold.databrick import Databrick


class TheFold:
    """
    The Monarch's data storage facility, modelled as a weighted
    undirected graph.

    Nodes are databricks plus three special locations: the Entrance
    (where the crew goes in), the Power Unit (which every databrick
    must be able to reach through the network, which is why The Fold
    is always connected), and the Roof (where the freighter waits).
    Every connection is protected by a number of firewalls, drawn
    uniformly between 1 and the configured maximum.
    """

    def __init__(self, config: dict) -> None:
        """
        Builds The Fold from a validated configuration dictionary.

        The generator first links every node into a random spanning
        tree (guaranteeing that each databrick can reach the Power
        Unit), then adds further random connections until the
        configured num_edges is met.

        @param config: The validated configuration dictionary.
        @returns: None
        """
        rng = random.Random(config["seed"])
        n = config["num_databricks"]

        # -- nodes: Entrance, d1..dn, Power Unit, Roof --------------
        self.entrance = Vertex(0, "Entrance")
        self.databricks: list[Databrick] = [
            Databrick(i,
                      rng.randint(*config["records_range"]),
                      rng.randint(*config["brick_weight_range"]),
                      rng.randint(*config["brick_volume_range"]))
            for i in range(1, n + 1)
        ]
        self.power_unit = Vertex(n + 1, "Power Unit")
        self.roof = Vertex(n + 2, "Roof")

        nodes: list[Vertex] = ([self.entrance] + list(self.databricks)
                               + [self.power_unit, self.roof])

        # -- graph representation ----------------------------------
        if config["graph_type"] == "matrix":
            self.graph: Graph = AdjacencyMatrix()
        else:
            self.graph = AdjacencyList()
        for node in nodes:
            self.graph.add_vertex(node)

        # -- connections -------------------------------------------
        max_f = config["max_firewalls"]
        total = len(nodes)

        # Random spanning tree first: every node joins an
        # already-connected node, so the network is connected.
        shuffled = nodes[:]
        rng.shuffle(shuffled)
        for i in range(1, total):
            partner = shuffled[rng.randrange(i)]
            self.graph.add_edge(shuffled[i], partner,
                                rng.randint(1, max_f))

        # Then add further connections up to the requested count.
        target = config["num_edges"]
        pairs = [(a, b) for a in range(total) for b in range(a + 1, total)]
        rng.shuffle(pairs)
        for a, b in pairs:
            if self.graph.num_edges() >= target:
                break
            self.graph.add_edge(nodes[a], nodes[b], rng.randint(1, max_f))

    def get_graph(self) -> Graph:
        """
        @returns: The network as a Graph.
        """
        return self.graph

    def get_databricks(self) -> list[Databrick]:
        """
        @returns: All databrick nodes (the haul the crew recovers),
                  excluding the three special locations.
        """
        return list(self.databricks)
