# -------------------------------------------------
# DO NOT CHANGE THIS FILE.
# Base class for graph edges (connections of The Fold).
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from graph.vertex import Vertex


class Edge:
    """
    A connection between two nodes of The Fold.

    The weight of an edge is the number of firewalls protecting the
    connection: a positive integer. Connections work in both directions,
    so Edge(u, v) and Edge(v, u) describe the same connection.
    """

    def __init__(self, u: Vertex, v: Vertex, weight: int) -> None:
        """
        Initialises an Edge between two vertices.

        @param u: The first vertex of the edge.
        @param v: The second vertex of the edge.
        @param weight: The number of firewalls on this connection
                       (a positive integer).
        @returns: None
        """
        self.u = u
        self.v = v
        self.weight = weight

    def __repr__(self) -> str:
        """
        Returns a string representation of the edge.

        @returns: A string of the form 'd1 --3-- d4'.
        """
        return f"{self.u} --{self.weight}-- {self.v}"

    def __hash__(self) -> int:
        """
        Hashes the edge symmetrically: Edge(u, v) and Edge(v, u)
        produce the same hash.

        @returns: Hash of the unordered pair of vertex indices.
        """
        return hash(frozenset({self.u.index, self.v.index}))

    def __eq__(self, other: object) -> bool:
        """
        Two edges are equal when they connect the same pair of
        vertices, in either order.

        @param other: The object to compare against.
        @returns: True if both edges join the same pair of vertices.
        """
        if not isinstance(other, Edge):
            return NotImplemented
        return (frozenset({self.u.index, self.v.index})
                == frozenset({other.u.index, other.v.index}))
