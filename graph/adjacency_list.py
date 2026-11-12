# -------------------------------------------------
# EDIT THIS FILE TO IMPLEMENT TASK A.
# Adjacency list implementation of the Graph ABC.
#
# __author__ = 'Maleka Ramchandani'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from graph.graph import Graph
from graph.vertex import Vertex
from graph.edge import Edge


class LinkedListNode:
    """
    A single entry in the linked list used by the AdjacencyList.

    Each entry stores a neighbouring vertex, the number of firewalls
    on the connection to that neighbour, and a pointer to the next
    entry in the chain. The chain for a given vertex, followed to
    its end, is that vertex's adjacency list.
    """

    def __init__(self, neighbour: Vertex, weight: int,
                 next_node: 'LinkedListNode | None' = None) -> None:
        """
        Initialises a LinkedListNode.

        @param neighbour: The neighbouring vertex this entry records.
        @param weight: The number of firewalls on the connection.
        @param next_node: The next entry in the chain, or None if this
                          is the last entry.
        @returns: None
        """
        self.neighbour = neighbour
        self.weight = weight
        self.next = next_node

    def __repr__(self) -> str:
        """
        Renders this entry and the remainder of its chain.

        @returns: A string of the form '(d1, 3) -> (d4, 2) -> None'.
        """
        return f"({self.neighbour}, {self.weight}) -> {self.next!r}"


class AdjacencyList(Graph):
    """
    An adjacency list representation of The Fold.

    The structure is an array of linked lists: one chain per vertex,
    where each entry in a vertex's chain records one real connection.
    Only connections that actually exist are stored.
    """

    def __init__(self) -> None:
        """
        Initialises an empty adjacency list graph. Internally keeps
        one chain head per vertex (initially None) plus the vertex
        objects themselves.

        @returns: None
        """
        self._heads: list[LinkedListNode | None] = []
        self._vertices: list[Vertex] = []
        self._index_of: dict[int, int] = {}   # vertex.index -> slot
        self._num_edges: int = 0

    def _pos(self, vertex: Vertex) -> int | None:
        """
        Looks up the slot of a vertex in the array of chains.

        @param vertex: The vertex to look up.
        @returns: The slot as an integer, or None if unknown.
        """
        return self._index_of.get(vertex.index)

    def _find_node(self, slot: int, neighbour: Vertex) -> LinkedListNode | None:
        """
        Walks one chain looking for the entry that records a given
        neighbour.

        @param slot: The slot whose chain should be walked.
        @param neighbour: The neighbour to look for.
        @returns: The matching LinkedListNode, or None if the chain
                  holds no entry for that neighbour.
        """
        node = self._heads[slot]
        while node is not None:
            if node.neighbour == neighbour:
                return node
            node = node.next
        return None

    def _delete_node(self, slot: int, neighbour: Vertex) -> bool:
        """
        Unlinks the entry for a given neighbour from one chain,
        re-joining the chain around it.

        @param slot: The slot whose chain should be edited.
        @param neighbour: The neighbour whose entry is to be removed.
        @returns: True if an entry was found and unlinked; False if
                  the chain holds no entry for that neighbour.
        """

        prev = None # prev refers to one box behind node, it starts as None because nothing comes before the first box
        node = self._heads[slot] #starts at the first box
        while node is not None: #goes through the chain until we reach the end
            if node.neighbour == neighbour:
                if prev is None:               #deleted the first box of the chain and makes the second one as head
                    self._heads[slot]= node.next
                else:
                    prev.next = node.next #deleting a middle or last box, if it was the last box of the chain, prev becomes the new end of the chain
                return True
            prev = node
            node = node.next #prev must be updated first before node moves on 
       
        return False #nothing removed if no neighbour found

    def add_vertex(self, vertex: Vertex) -> bool:
        """
        Adds a vertex with an empty chain.

        @param vertex: The vertex to add.
        @returns: True if added; False if a vertex with the same index
                  already exists.
        """
        if vertex.index in self._index_of:
            return False
        self._index_of[vertex.index] = len(self._vertices)
        self._vertices.append(vertex)
        self._heads.append(None)
        return True

    def add_edge(self, u: Vertex, v: Vertex, weight: int) -> bool:
        """
        Adds an undirected connection by prepending a new entry to
        both u's chain and v's chain.

        @param u: The first vertex.
        @param v: The second vertex.
        @param weight: The number of firewalls (must be at least 1).
        @returns: True if added; False if either vertex is unknown,
                  u equals v, the weight is below 1, or the connection
                  already exists.
        """
        slot_v=self._pos(v)
        slot_u= self._pos(u)
        # if input is invalid
        if slot_u is None or slot_v is None:
            return False
        if u == v:
            return False
        if weight <1:
            return False
        if self._find_node(slot_u,v) is not None:
            return False
        # Add a box to u's chain recording v
        new_u= LinkedListNode(v, weight, self._heads[slot_u])
        self._heads[slot_u]= new_u
        #Add a box to v's chain recording u
        new_v = LinkedListNode(u, weight, self._heads[slot_v])
        self._heads[slot_v] = new_v

        self._num_edges += 1
        return True
        

    def remove_edge(self, u: Vertex, v: Vertex) -> bool:
        """
        Removes a connection by unlinking the matching entry from
        both chains.

        @param u: The first vertex.
        @param v: The second vertex.
        @returns: True if the connection existed and was removed;
                  False otherwise.
        """
        slot_u= self._pos(u)
        slot_v= self._pos(v)
        if slot_u is None or slot_v is None: #if the vertex doesnt exist
            return False
        if self._find_node(slot_u,v) is None:
            return False #no edge, so nothing to remove
        else:
            self._delete_node(slot_u,v) #remove v's box from u's chain
            self._delete_node(slot_v,u)#remove u's box from v
            self._num_edges-=1
            return True

    def update_edge_weight(self, u: Vertex, v: Vertex, weight: int) -> bool:
        """
        Changes the number of firewalls recorded for an existing
        connection, in both chains.

        @param u: The first vertex.
        @param v: The second vertex.
        @param weight: The new number of firewalls (must be at least 1).
        @returns: True if the connection existed and was updated;
                  False otherwise.
        """
        slot_u= self._pos(u)
        slot_v= self._pos(v)
        #check if vertex exists
        if slot_v is None or slot_u is None:
            return False
        if weight<1:
            return False
        #create variable for node u and v
        box_u=  self._find_node(slot_u,v) 
        box_v= self._find_node(slot_v,u)
        #check if connection exists
        if box_u is None:
            return False
        else:
            box_u.weight= weight #update the weight
            box_v.weight= weight
            return True


    def get_vertices(self) -> list[Vertex]:
        """
        Returns all vertices in insertion order.

        @returns: A list of Vertex objects.
        """
        return list(self._vertices)

    def get_edges(self) -> list[Edge]:
        """
        Walks every chain and returns each connection exactly once
        (a connection is emitted only from the endpoint with the
        smaller slot).

        @returns: A list of Edge objects.
        """
        edges: list[Edge] = []
        for slot, head in enumerate(self._heads):
            node = head
            while node is not None:
                other = self._pos(node.neighbour)
                if other is not None and slot < other:
                    edges.append(Edge(self._vertices[slot],
                                      node.neighbour, node.weight))
                node = node.next
        return edges

    def get_neighbours(self, vertex: Vertex) -> list[tuple[Vertex, int]]:
        """
        Walks one chain and returns each entry as a
        (neighbour, weight) pair.

        @param vertex: The vertex whose neighbours are to be returned.
        @returns: A list of (neighbour, weight) tuples; empty if the
                  vertex is unknown.
        """
        list_of_neighbours=[]
        box= self._pos(vertex)
        if box is None:         #if vertex doesnt exist
            list_of_neighbours=[]
        else:
            node= self._heads[box]     #start from the head
            while node is not None:
                list_of_neighbours.append((node.neighbour, node.weight)) #add each node
                node= node.next
        return list_of_neighbours


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
        Walks u's chain looking for v.

        @param u: The first vertex.
        @param v: The second vertex.
        @returns: The number of firewalls, or 0 if no connection
                  exists or either vertex is unknown (matching the
                  matrix's behaviour).
        """
        # find which slot u's chain is stored in
        slot_u = self._pos(u)
        # u was never added, so there can't be a connection hence return 0
        if slot_u is None:
            return 0
        # look through u's chain for the box that records v
        box = self._find_node(slot_u, v)
        # no box for v means no connection, so return 0 (same as the matrix)
        if box is None:
            return 0
        # the connection exists, so return the firewall count stored in the box
        return box.weight

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
        Renders every chain on its own line, for use with the
        print_struct configuration option.

        @returns: A multi-line string picture of the structure.
        """
        out = ""
        for slot, v in enumerate(self._vertices):
            out += f"[{slot}] {v.name}: {self._heads[slot]!r}\n"
        return out
