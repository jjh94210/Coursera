"""
Provided code for application portion of module 1

Helper class for implementing efficient version
of DPA algorithm
"""

# general imports
import random
import matplotlib.pyplot as plt

class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

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

def DPA(n, m):
    graph = make_complete_graph(m)
    trial_class = DPATrial(m)
    for dummy_node in range(m, n):
        added_node_list = trial_class.run_trial(m)
        graph[dummy_node] = added_node_list
    return graph

DPA_graph = DPA(28000, 13)
normalized = normalize_degree_distribution(in_degree_distribution(DPA_graph))

x_data = normalized.keys()
y_data = normalized.values()

plt.figure()
plt.xscale('log')
plt.yscale('log')
plt.scatter(x_data[1:], y_data[1:])
plt.title('In-degree distribution for the DPA graph(log/log scale)')
plt.xlabel('Number of degree')
plt.ylabel('Normalized distribution of degree')
plt.show()
