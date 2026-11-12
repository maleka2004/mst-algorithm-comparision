# -------------------------------------------------
# DO NOT CHANGE THIS FILE.
# Union-find (disjoint set) structure, provided for Task B.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from graph.vertex import Vertex


class UnionFind:
    """
    Tracks which vertices are already linked into the same group.

    Supports two operations: find(v), which returns the identifier of
    the group v currently belongs to, and union(u, v), which merges
    the groups of u and v. Two vertices are already connected exactly
    when find gives the same identifier for both.
    """

    def __init__(self, vertices: list[Vertex]) -> None:
        """
        Initialises the structure with every vertex in its own group.

        @param vertices: The vertices to track.
        @returns: None
        """
        self._parent: dict[int, int] = {v.index: v.index for v in vertices}
        self._rank: dict[int, int] = {v.index: 0 for v in vertices}

    def find(self, v: Vertex) -> int:
        """
        Returns the identifier of the group that v belongs to,
        flattening the internal chain as it goes.

        @param v: The vertex to look up.
        @returns: The integer identifier of v's group.
        """
        root = v.index
        while self._parent[root] != root:
            root = self._parent[root]
        # Path compression: point everything on the walk at the root.
        i = v.index
        while self._parent[i] != root:
            self._parent[i], i = root, self._parent[i]
        return root

    def union(self, u: Vertex, v: Vertex) -> None:
        """
        Merges the groups containing u and v. Has no effect when the
        two are already in the same group.

        @param u: The first vertex.
        @param v: The second vertex.
        @returns: None
        """
        ru, rv = self.find(u), self.find(v)
        if ru == rv:
            return
        if self._rank[ru] < self._rank[rv]:
            ru, rv = rv, ru
        self._parent[rv] = ru
        if self._rank[ru] == self._rank[rv]:
            self._rank[ru] += 1
