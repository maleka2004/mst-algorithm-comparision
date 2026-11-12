# -------------------------------------------------
# DO NOT CHANGE THIS FILE.
# Abstract base class for graph implementations.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from abc import ABC, abstractmethod
from graph.vertex import Vertex
from graph.edge import Edge


class Graph(ABC):
    """
    Abstract base class for all graph representations of The Fold.

    Defines the interface that every concrete representation must
    follow. Algorithms should program against this interface only,
    so that they work correctly with any representation (adjacency
    matrix or adjacency list) without modification.

    Defensive behaviour required of every implementation:
      * add_vertex refuses a vertex whose index is already present.
      * add_edge refuses self-loops, unknown vertices, weights below 1,
        and connections that already exist.
      * remove_edge / update_edge_weight refuse unknown vertices and
        connections that do not exist.
      * All mutations keep the graph undirected: whatever holds for
        (u, v) must equally hold for (v, u).
    """

    @abstractmethod
    def add_vertex(self, vertex: Vertex) -> bool:
        """
        Adds a vertex to the graph.

        @param vertex: The vertex to add.
        @returns: True if the vertex was added; False if a vertex with
                  the same index is already in the graph.
        """
        pass

    @abstractmethod
    def add_edge(self, u: Vertex, v: Vertex, weight: int) -> bool:
        """
        Adds an undirected connection between u and v with the given
        number of firewalls. Both directions must be recorded.

        @param u: The first vertex.
        @param v: The second vertex.
        @param weight: The number of firewalls (must be at least 1).
        @returns: True if the connection was added; False if either
                  vertex is unknown, u equals v, the weight is below 1,
                  or the connection already exists.
        """
        pass

    @abstractmethod
    def remove_edge(self, u: Vertex, v: Vertex) -> bool:
        """
        Removes the connection between u and v from both vertices.

        @param u: The first vertex.
        @param v: The second vertex.
        @returns: True if the connection existed and was removed;
                  False otherwise.
        """
        pass

    @abstractmethod
    def update_edge_weight(self, u: Vertex, v: Vertex, weight: int) -> bool:
        """
        Changes the number of firewalls on an existing connection,
        in both directions.

        @param u: The first vertex.
        @param v: The second vertex.
        @param weight: The new number of firewalls (must be at least 1).
        @returns: True if the connection existed and was updated;
                  False otherwise.
        """
        pass

    @abstractmethod
    def get_vertices(self) -> list[Vertex]:
        """
        Returns all vertices in the graph.

        @returns: A list of all Vertex objects in the graph.
        """
        pass

    @abstractmethod
    def get_edges(self) -> list[Edge]:
        """
        Returns all connections in the graph. Each undirected
        connection appears exactly once.

        @returns: A list of all Edge objects in the graph.
        """
        pass

    @abstractmethod
    def get_neighbours(self, vertex: Vertex) -> list[tuple[Vertex, int]]:
        """
        Returns every vertex joined directly to the given vertex,
        together with the number of firewalls on each connection.

        @param vertex: The vertex whose neighbours are to be returned.
        @returns: A list of (neighbour, weight) tuples.
        """
        pass

    @abstractmethod
    def has_edge(self, u: Vertex, v: Vertex) -> bool:
        """
        Checks whether a connection exists between two vertices.

        @param u: The first vertex.
        @param v: The second vertex.
        @returns: True if a connection exists between u and v.
        """
        pass

    @abstractmethod
    def get_edge_weight(self, u: Vertex, v: Vertex) -> int:
        """
        Returns the number of firewalls on the connection between two
        vertices. By the convention of the assignment, a value of 0
        means there is no direct connection.

        @param u: The first vertex.
        @param v: The second vertex.
        @returns: The number of firewalls as an integer, or 0 if no
                  connection exists.
        """
        pass

    @abstractmethod
    def num_vertices(self) -> int:
        """
        Returns the number of vertices in the graph.

        @returns: The number of vertices as an integer.
        """
        pass

    @abstractmethod
    def num_edges(self) -> int:
        """
        Returns the number of connections in the graph. Each
        undirected connection is counted once.

        @returns: The number of connections as an integer.
        """
        pass
