"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2
import math
import matplotlib.pyplot as plt

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"
CITATION_PATH = "alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

def load_graph_local(graph_path):
    """
    Function that loads a graph given the PATH
    for a text representation of the graph

    Returns a dictionary that models a graph
    """
    graph_file = open(graph_path, 'r')
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]

    print "Loaded graph with", len(graph_lines), "nodes"

    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

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

#citation_graph = load_graph(CITATION_URL)
citation_graph = load_graph_local(CITATION_PATH)
normalized = normalize_degree_distribution(in_degree_distribution(citation_graph))

x_data = normalized.keys()
y_data = normalized.values()

plt.figure()
plt.xscale('log')
plt.yscale('log')
plt.scatter(x_data[1:], y_data[1:])
plt.title('In-degree distribution for the citation graph(log/log scale)')
plt.xlabel('Number of citation(degree)')
plt.ylabel('Normalized distribution of citation')
plt.show()
