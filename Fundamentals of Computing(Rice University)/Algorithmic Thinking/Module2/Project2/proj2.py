"""
Project component of Module 2

Python code that implements breadth-first search.
Compute the set of connected components (CCs) of an undirected graph as well as determine the size of its largest connected component.
Computes the resilience of a graph (measured by the size of its largest connected component) as a sequence of nodes are deleted from the graph.
"""

from collections import deque
import random

def bfs_visited(ugraph, start_node):
    """
    Takes the undirected graph(ugraph) and the node(start_node)
    and returns the set consisting of all nodes that are visited by a breadth-first search that starts at start_node.
    """
    queue = deque()
    visited = set([start_node])
    queue.appendleft(start_node)
    while len(queue):
        j_node = queue.pop()
        for h_node in ugraph[j_node]:
            if h_node not in visited:
                visited.add(h_node)
                queue.appendleft(h_node)
    return visited

def cc_visited(ugraph):
    """
    Takes the undirected graph(ugraph) and returns a list of sets,
    where each set consists of all the nodes (and nothing else) in a connected component, and there is exactly one set in the list for each connected component in ugraph and nothing else.
    """
    remaining_nodes = set(ugraph.keys())
    con_comp = []
    while len(remaining_nodes):
        i_node = random.choice(list(remaining_nodes))
        connected_set = bfs_visited(ugraph, i_node)
        con_comp.append(connected_set)
        remaining_nodes.difference_update(connected_set)
    return con_comp

def largest_cc_size(ugraph):
    """
    Takes the undirected graph(ugraph) and returns the size (an integer) of the largest connected component in ugraph.
    """
    if ugraph == {}:
        return 0
    con_comp = cc_visited(ugraph)
    cc_size = []
    for dummy_set in con_comp:
        cc_size.append(len(dummy_set))
    return max(cc_size)

def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph(ugraph), a list of nodes(attack_order) and iterates through the nodes in attack_order.
    For each node in the list, the function removes the given node and its edges from the graph and then computes the size of the largest connected component for the resulting graph.
    The function should return a list whose k+1th entry is the size of the largest connected component in the graph after the removal of the first k nodes in attack_order. The first entry (indexed by zero) is the size of the largest connected component in the original graph.
    """
    temp_ugraph = ugraph
    resilience = []
    resilience.append(largest_cc_size(temp_ugraph))
    for dummy_order in attack_order:
        if len(temp_ugraph[dummy_order]):
            for dummy_node in temp_ugraph[dummy_order]:
                temp_ugraph[dummy_node].remove(dummy_order)
        temp_ugraph.pop(dummy_order)
        print resilience
        print temp_ugraph
        resilience.append(largest_cc_size(temp_ugraph))
    return resilience
