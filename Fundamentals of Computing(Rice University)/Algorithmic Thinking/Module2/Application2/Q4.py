"""
Provided code for Application portion of Module 2
"""

# general imports
import urllib2
import random
import time
import math

# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
import matplotlib.pyplot as plt
from collections import deque

############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
NETWORK_PATH = "alg_rf7.txt"

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

##########################################################
# Code for make undirected ER Graph

def undirected_ER(n, p):
    ER_graph = {}
#    complete_edge_list = []
    for target_node in range(n):
        ER_graph[target_node] = set([])
#    for first_node in range(n-1):
#        for second_node in range(first_node + 1, n):
#            complete_edge_list.append((first_node, second_node))
#    for temp_node in complete_edge_list:
#        if random.random() < p:
#            ER_graph[first_node].add(second_node)
#            ER_graph[second_node].add(first_node)

    for target_node in range(n):
        temp_node_list = range(n)
        temp_node_list.remove(target_node)
        for temp_node in ER_graph.keys():
            if target_node in ER_graph[temp_node]:
                temp_node_list.remove(temp_node)
        for dummy_node in temp_node_list:
            if random.random() < p/2:
                ER_graph[target_node].add(dummy_node)
                ER_graph[dummy_node].add(target_node)

    return ER_graph

##########################################################
# Code for make UPA graph
"""
Provided code for application portion of module 2

Helper class for implementing efficient version
of UPA algorithm
"""

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
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

def UPA(n, m):
    graph = make_complete_graph(m)
    trial_class = UPATrial(m)
    for dummy_node in range(m, n):
        added_node_list = trial_class.run_trial(m)
        graph[dummy_node] = added_node_list
        for dummy_rev_node in added_node_list:
            graph[dummy_rev_node].add(dummy_node)

    return graph

##########################################################
# Code for analysis graph
"""
Project component of Module 2

Python code that implements breadth-first search.
Compute the set of connected components (CCs) of an undirected graph as well as determine the size of its largest connected component.
Computes the resilience of a graph (measured by the size of its largest connected component) as a sequence of nodes are deleted from the graph.
"""

def random_order(n):
    order = range(n)
    random.shuffle(order)
    return order

def average_degree(graph):
    sum_of_degree = 0
    for dummy_node in graph.keys():
        sum_of_degree += len(graph[dummy_node])
    return (float(sum_of_degree) / len(graph.keys()))

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
    temp_ugraph = copy_graph(ugraph)
    resilience = []
    resilience.append(largest_cc_size(temp_ugraph))
    for dummy_order in attack_order:
        if dummy_order in temp_ugraph.keys():
            delete_node(temp_ugraph, dummy_order)
        resilience.append(largest_cc_size(temp_ugraph))
    return resilience

##########################################################
# Code for FastTargetedOrder
def fast_targeted_order(ugraph):
    graph = copy_graph(ugraph)
    node_size = len(graph.keys())
    degree_sets = {}
    for dummy_node in range(node_size):
        degree_sets[dummy_node] = set([])
    for dummy_node in range(node_size):
        if dummy_node in graph.keys():
            degree = len(graph[dummy_node])
            degree_sets[degree].add(dummy_node)
    targeted_order = []
    dummy_i = 0
    for dummy_k in range(node_size - 1, -1, -1):
        while degree_sets[dummy_k] != set([]):
            dummy_node = random.choice(list(degree_sets[dummy_k]))
            degree_sets[dummy_k].remove(dummy_node)
            for dummy_v in graph[dummy_node]:
                #print graph[dummy_node]
                #print degree_sets
                #print dummy_v
                degree = len(graph[dummy_v])
                degree_sets[degree].remove(dummy_v)
                degree_sets[degree - 1].add(dummy_v)
            targeted_order.append(dummy_node)
            dummy_i += 1
            delete_node(graph, dummy_node)
    return targeted_order

##########################################################
# Code for TargetedOrder
def targeted_order(ugraph):
    graph = copy_graph(ugraph)
    targeted_order = []
    while len(graph.keys()):
        max_degree = len(graph[graph.keys()[0]])
        max_node_list = []
        for dummy_node in graph.keys():
            if max_degree == len(graph[dummy_node]):
                max_node_list.append(dummy_node)
            if max_degree < len(graph[dummy_node]):
                max_degree = len(graph[dummy_node])
                max_node_list = [dummy_node]
        remove_node = random.choice(max_node_list)
        targeted_order.append(remove_node)
        delete_node(graph, remove_node)
    return targeted_order

computer_network_graph = load_graph_local(NETWORK_PATH)
ER_graph = undirected_ER(1239, 0.004)
UPA_graph = UPA(1239, 3)

print average_degree(computer_network_graph)
print average_degree(ER_graph)
print average_degree(UPA_graph)

attack_order_CN = targeted_order(computer_network_graph)
attack_order_ER = fast_targeted_order(ER_graph)
attack_order_UPA = fast_targeted_order(UPA_graph)

attack_times = range(1241)
attack_times = attack_times[1:]
computer_network_resilience = compute_resilience(computer_network_graph, attack_order_CN)
ER_graph_resilience = compute_resilience(ER_graph, attack_order_ER)
UPA_graph_resilience = compute_resilience(UPA_graph, attack_order_UPA)

plt.figure()
plt.plot(attack_times, computer_network_resilience, '-b', label = 'computer_network')
plt.plot(attack_times, ER_graph_resilience, '-g', label = 'ER_graph(p=0.004)')
plt.plot(attack_times, UPA_graph_resilience, '-r', label = 'UPA_graph(m=3)')
plt.legend(loc = 'upper right')
plt.title('Three undirected graphs resilience for targeted attack order')
plt.xlabel('Number of nodes removed')
plt.ylabel('Size of the largest connect component')
plt.show()
