"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import math
import random
import matplotlib.pyplot as plt

###################################
# Code for make ER Graph

def ER(n, p):
    ER_graph = {}
    for target_node in range(n):
        ER_graph[target_node] = set([])
        temp_node_list = range(n)
        temp_node_list.remove(target_node)
        for dummy_node in temp_node_list:
            if random.random() < p:
                ER_graph[target_node].add(dummy_node)

    return ER_graph

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

def normalize_degree_distribution(distribution):
    """
    Takes a unnormalized distribution and computes the normalized distribution
    of the in-degree of the graph
    """
    normalized = {}
    distribution_sum = 0
    for dummy_degree in distribution.keys():
        distribution_sum += distribution[dummy_degree]
    for dummy_degree in distribution.keys():
        normalized[dummy_degree] = float(distribution[dummy_degree]) / distribution_sum
    return normalized

n = 10000
p = 0.5
graph = ER(n, p)
normalized = normalize_degree_distribution(in_degree_distribution(graph))

x_data = normalized.keys()
y_data = normalized.values()

plt.figure()
# plt.xscale('log')
# plt.yscale('log')
plt.scatter(x_data[1:], y_data[1:])
plt.title('In-degree distribution for the ER graph(log/log scale)')
plt.xlabel('Number of degree')
plt.ylabel('Normalized distribution of degree')
plt.show()
