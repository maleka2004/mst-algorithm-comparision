# -------------------------------------------------
# DO NOT CHANGE THIS FILE.
# Adjacency matrix implementation of the Graph ABC.
# This is the reference representation you are given.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from graph.graph import Graph
from graph.vertex import Vertex
from graph.edge import Edge


class AdjacencyMatrix(Graph):
    """
    An adjacency matrix representation of The Fold.

    The matrix is an array of arrays. Cell (i, j) holds the number of
    firewalls on the connection between the vertices with indices i
    and j, or 0 if there is no direct connection. Because the graph
    is undirected, the matrix is symmetric: cell (i, j) always equals
    cell (j, i).
    """

    def __init__(self) -> None:
        """
        Initialises an empty adjacency matrix graph.

        @returns: None
        """
        self._matrix: list[list[int]] = []
        self._vertices: list[Vertex] = []
        self._index_of: dict[int, int] = {}   # vertex.index -> row position
        self._num_edges: int = 0

    def _pos(self, vertex: Vertex) -> int | None:
        """
        Looks up the matrix row/column position of a vertex.

        @param vertex: The vertex to look up.
        @returns: The position as an integer, or None if the vertex
                  is not in the graph.
        """
        return self._index_of.get(vertex.index)

    def add_vertex(self, vertex: Vertex) -> bool:
        """
        Adds a vertex, growing the matrix by one row and one column
        filled with zeros (no connections yet).

        @param vertex: The vertex to add.
        @returns: True if added; False if a vertex with the same index
                  already exists.
        """
        if vertex.index in self._index_of:
            return False
        self._index_of[vertex.index] = len(self._vertices)
        self._vertices.append(vertex)
        for row in self._matrix:
            row.append(0)
        self._matrix.append([0] * len(self._vertices))
        return True

    def add_edge(self, u: Vertex, v: Vertex, weight: int) -> bool:
        """
        Adds an undirected connection by writing the weight into both
        cell (u, v) and cell (v, u).

        @param u: The first vertex.
        @param v: The second vertex.
        @param weight: The number of firewalls (must be at least 1).
        @returns: True if added; False if either vertex is unknown,
                  u equals v, the weight is below 1, or the connection
                  already exists.
        """
        pu, pv = self._pos(u), self._pos(v)
        if pu is None or pv is None or pu == pv or weight < 1:
            return False
        if self._matrix[pu][pv] != 0:
            return False
        self._matrix[pu][pv] = weight
        self._matrix[pv][pu] = weight
        self._num_edges += 1
        return True

    def remove_edge(self, u: Vertex, v: Vertex) -> bool:
        """
        Removes a connection by zeroing both cell (u, v) and (v, u).

        @param u: The first vertex.
        @param v: The second vertex.
        @returns: True if the connection existed and was removed;
                  False otherwise.
        """
        pu, pv = self._pos(u), self._pos(v)
        if pu is None or pv is None or self._matrix[pu][pv] == 0:
            return False
        self._matrix[pu][pv] = 0
        self._matrix[pv][pu] = 0
        self._num_edges -= 1
        return True

    def update_edge_weight(self, u: Vertex, v: Vertex, weight: int) -> bool:
        """
        Overwrites the weight of an existing connection in both cells.

        @param u: The first vertex.
        @param v: The second vertex.
        @param weight: The new number of firewalls (must be at least 1).
        @returns: True if the connection existed and was updated;
                  False otherwise.
        """
        pu, pv = self._pos(u), self._pos(v)
        if pu is None or pv is None or weight < 1:
            return False
        if self._matrix[pu][pv] == 0:
            return False
        self._matrix[pu][pv] = weight
        self._matrix[pv][pu] = weight
        return True

    def get_vertices(self) -> list[Vertex]:
        """
        Returns all vertices in insertion order.

        @returns: A list of Vertex objects.
        """
        return list(self._vertices)

    def get_edges(self) -> list[Edge]:
        """
        Scans the upper triangle of the matrix and returns each
        connection exactly once.

        @returns: A list of Edge objects.
        """
        edges: list[Edge] = []
        n = len(self._vertices)
        for i in range(n):
            for j in range(i + 1, n):
                if self._matrix[i][j] != 0:
                    edges.append(Edge(self._vertices[i], self._vertices[j],
                                      self._matrix[i][j]))
        return edges

    def get_neighbours(self, vertex: Vertex) -> list[tuple[Vertex, int]]:
        """
        Scans one full row of the matrix and returns every non-zero
        entry as a (neighbour, weight) pair.

        @param vertex: The vertex whose neighbours are to be returned.
        @returns: A list of (neighbour, weight) tuples; empty if the
                  vertex is unknown.
        """
        p = self._pos(vertex)
        if p is None:
            return []
        result: list[tuple[Vertex, int]] = []
        for j, w in enumerate(self._matrix[p]):
            if w != 0:
                result.append((self._vertices[j], w))
        return result

    def has_edge(self, u: Vertex, v: Vertex) -> bool:
        """
        Checks whether a connection exists between two vertices.

        @param u: The first vertex.
        @param v: The second vertex.
        @returns: True if a connection exists.
        """
        return self.get_edge_weight(u, v) != 0

    def get_edge_weight(self, u: Vertex, v: Vertex) -> int:
        """
        Reads cell (u, v) of the matrix.

        @param u: The first vertex.
        @param v: The second vertex.
        @returns: The number of firewalls, or 0 if no connection
                  exists or either vertex is unknown.
        """
        pu, pv = self._pos(u), self._pos(v)
        if pu is None or pv is None:
            return 0
        return self._matrix[pu][pv]

    def num_vertices(self) -> int:
        """
        @returns: The number of vertices as an integer.
        """
        return len(self._vertices)

    def num_edges(self) -> int:
        """
        @returns: The number of connections as an integer, each
                  counted once.
        """
        return self._num_edges

    def __repr__(self) -> str:
        """
        Renders the matrix with row and column headers, for use with
        the print_struct configuration option.

        @returns: A multi-line string picture of the matrix.
        """
        names = [v.name for v in self._vertices]
        width = max((len(n) for n in names), default=1) + 1
        out = " " * width + "".join(f"{n:>{width}}" for n in names) + "\n"
        for i, row in enumerate(self._matrix):
            out += f"{names[i]:>{width}}" + "".join(
                f"{w:>{width}}" for w in row) + "\n"
        return out
