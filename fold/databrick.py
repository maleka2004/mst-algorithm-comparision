# -------------------------------------------------
# DO NOT CHANGE THIS FILE.
# A databrick: one of the Monarch's data servers.
#
# __author__ = 'Edward Small'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from graph.vertex import Vertex


class Databrick(Vertex):
    """
    A databrick node of The Fold.

    Each databrick stores the personal records of many citizens.
    Deleting a databrick's data frees every one of those people from
    their debt contract, so a brick's value is the number of records
    it holds. It also has a physical weight and volume, which matter
    when loading the freighter in Task D.
    """

    def __init__(self, index: int, records: int,
                 weight: int, volume: int) -> None:
        """
        Initialises a Databrick.

        @param index: The unique integer index of this node.
        @param records: The number of citizen records stored (the
                        brick's value).
        @param weight: The physical weight in kilograms.
        @param volume: The physical volume in litres.
        @returns: None
        """
        super().__init__(index, f"d{index}")
        self.records = records
        self.weight = weight
        self.volume = volume

    def __repr__(self) -> str:
        """
        Returns a compact description of the databrick.

        @returns: A string such as 'd3(42k rec, 4kg, 3L)'.
        """
        return f"{self.name}({self.records} rec, {self.weight}kg, {self.volume}L)"
