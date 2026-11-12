# -------------------------------------------------
# EDIT THIS FILE TO IMPLEMENT TASK B.
# Kruskal's algorithm.
#
# __author__ = 'Maleka Ramchandani'
# __project__ = "Neuromancer: Hacking with Graphs"
# __copyright__ = 'Copyright 2026, RMIT University'
# -------------------------------------------------

from graph.graph import Graph
from graph.edge import Edge
from mst.merge_sort import merge_sort
from mst.union_find import UnionFind


def kruskals(graph: Graph) -> tuple[list[Edge], int]:
    """
    Computes a minimum spanning tree of a connected graph using
    Kruskal's algorithm.

    Considers every connection from lightest to heaviest and keeps a
    connection whenever its two endpoints are not already linked by
    the connections kept so far. Stops once the tree holds every
    vertex.

    You are given two tools to use: merge_sort (mst/merge_sort.py) to
    order the connections, and UnionFind (mst/union_find.py) to decide
    whether two vertices are already linked.

    @param graph: The graph to span. Must be connected.
    @returns: A tuple of:
              - list[Edge]: the connections chosen for the tree.
              - int: the total number of firewalls across the tree.

    HINT: get_edges gives every connection; sort them, then add a
    connection only when its endpoints are not already joined.
    """
    # IMPLEMENT ME! (Task B)
    # Return the chosen connections and their total firewalls. The empty
    # return below is a valid placeholder so the program runs before you
    # start: it finds no tree.
    edges= graph.get_edges()
    vertices= graph.get_vertices()  
    if not edges:
        return [], 0
    sorted_edges= merge_sort(edges)
    group= UnionFind(vertices) #puts every vertex in its own group
    tree= [None] *(graph.num_vertices()-1) #create the list where all chosen  edges go
    added=0 #to track the count of additions made to tree
    total= 0 #running total of firewalls

    for edge in sorted_edges:
        if group.find(edge.u)!= group.find(edge.v): #if both vertex are not in the same group, add it to the tree and if its the same group it will create a loop
            group. union(edge.u, edge.v) #merge the two groups
            tree[added] = edge   #add it to the next free slot             
            added +=1
            total +=edge.weight
            if added == graph.num_vertices()-1: #at this point the tree is full, so stop
                break
    return tree, total 
    
