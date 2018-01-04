"""
Project #1

Representing directed graphs
Computing degree distributions
"""
# By Jaehwi Cho

EX_GRAPH0 = {0: set([1, 2]),
             1: set([]),
             2: set([])}

EX_GRAPH1 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3]),
             3: set([0]),
             4: set([1]),
             5: set([2]),
             6: set([])}

EX_GRAPH2 = {0: set([1, 4, 5]),
             1: set([2, 6]),
             2: set([3, 7]),
             3: set([7]),
             4: set([1]),
             5: set([2]),
             6: set([]),
             7: set([3]),
             8: set([1, 2]),
             9: set([0, 3, 4, 5, 6, 7])}

def make_complete_graph(num_nodes):
    """
    returns a dictionary corresponding to a complete directed graph
    with the specified number of nodes
    """
    graph = {}
    if num_nodes < 1:
        return graph
    else:
        for dummy_idx in range(num_nodes):
            temp_node = range(num_nodes)
            temp_node.remove(dummy_idx)
            graph[dummy_idx] = set(temp_node)
        return graph

def compute_in_degrees(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary)
    and computes the in-degrees for the nodes in the graph
    """
    degrees = {}
    for dummy_target_node in digraph.keys():
        temp_degree = 0
        for dummy_node in digraph.keys():
            if dummy_target_node in digraph[dummy_node]:
                temp_degree += 1
        degrees[dummy_target_node] = temp_degree
    return degrees

def in_degree_distribution(digraph):
    """
    Takes a directed graph digraph (represented as a dictionary)
    and computes the unnormalized distribution of the in-degrees of the graph
    """
    degrees = compute_in_degrees(digraph)
    distribution = {}
    for dummy_degree in degrees.values():
        if dummy_degree in distribution.keys():
            distribution[dummy_degree] += 1
        else:
            distribution[dummy_degree] = 1
    return distribution

# http://www.codeskulptor.org/#user43_zDlDjAEaiouuQrM.py
