# -------------------------------------------------
# DO NOT CHANGE THIS FILE.
# Base class for graph vertices (nodes of The Fold).
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------


class Vertex:
    """
    A node of The Fold.

    Most nodes are databricks; three are special locations
    (the Entrance, the Power Unit, and the Roof). A vertex is
    identified by a unique integer index and carries a display
    name used in printouts and the operation report.
    """

    def __init__(self, index: int, name: str | None = None) -> None:
        """
        Initialises a Vertex.

        @param index: The unique integer index of this vertex in the graph.
        @param name: Optional display name (e.g. 'Entrance', 'd7').
                     Defaults to 'd<index>' when omitted.
        @returns: None
        """
        self.index = index
        self.name = name if name is not None else f"d{index}"

    def __repr__(self) -> str:
        """
        Returns the display name of the vertex.

        @returns: A string such as 'd7' or 'Entrance'.
        """
        return self.name

    def __hash__(self) -> int:
        """
        Hashes the vertex by its index so vertices can be used
        as dictionary keys and in sets.

        @returns: Hash of the vertex index.
        """
        return hash(self.index)

    def __eq__(self, other: object) -> bool:
        """
        Two vertices are equal when they share the same index.

        @param other: The object to compare against.
        @returns: True if both are vertices with the same index.
        """
        if not isinstance(other, Vertex):
            return NotImplemented
        return self.index == other.index
