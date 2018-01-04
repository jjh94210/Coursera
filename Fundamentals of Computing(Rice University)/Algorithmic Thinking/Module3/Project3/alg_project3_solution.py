"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster



######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    dist_tuple = (float("inf"), -1, -1)
    for idx1 in range(len(cluster_list) - 1) :
        for idx2 in range(idx1 + 1, len(cluster_list)):
            temp_dist_tuple = pair_distance(cluster_list, idx1, idx2)
            if temp_dist_tuple[0] < dist_tuple[0]:
                dist_tuple = temp_dist_tuple
    return dist_tuple


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    size = len(cluster_list)
    if size <= 3:
        dist_tuple = slow_closest_pair(cluster_list)
    else:
        mid_idx = size / 2
        left_cluster_list = cluster_list[:mid_idx]
        right_cluster_list = cluster_list[mid_idx:]
        left_dist_tuple = fast_closest_pair(left_cluster_list)
        right_dist_tuple = fast_closest_pair(right_cluster_list)
        if left_dist_tuple[0] < right_dist_tuple[0]:
            dist_tuple = left_dist_tuple
        else:
            dist_tuple = (right_dist_tuple[0], right_dist_tuple[1] + mid_idx, right_dist_tuple[2] + mid_idx)
        horiz_center = (cluster_list[mid_idx - 1].horiz_center() + cluster_list[mid_idx].horiz_center()) / 2.0
        closest_pair = closest_pair_strip(cluster_list, horiz_center, dist_tuple[0])
        if closest_pair[0] < dist_tuple[0]:
            dist_tuple = closest_pair
    return dist_tuple


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    subcluster_list = []
    for idx in range(len(cluster_list)):
        if abs(cluster_list[idx].horiz_center() - horiz_center) < half_width:
            subcluster_list.append(idx)
    subcluster_list.sort(key = lambda idx: cluster_list[idx].vert_center())
    size = len(subcluster_list)
    dist_tuple = (float("inf"), -1, -1)
    for idx1 in range(size - 1):
        for idx2 in range(idx1 + 1, min(idx1 + 4, size)):
            temp_dist_tuple = pair_distance(cluster_list, subcluster_list[idx1], subcluster_list[idx2])
            if temp_dist_tuple[0] < dist_tuple[0]:
                dist_tuple = temp_dist_tuple
    return dist_tuple

 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        closest_pair = fast_closest_pair(cluster_list)
        cluster_list[closest_pair[1]].merge_clusters(cluster_list[closest_pair[2]])
        cluster_list.pop(closest_pair[2])
    return cluster_list


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
    copy_cluster_list = list(cluster_list)
    copy_cluster_list.sort(key = lambda cluster: cluster.total_population())
    copy_cluster_list.reverse()
    size = len(cluster_list)
    new_clusters = [alg_cluster.Cluster(set([]), copy_cluster_list[dummy_idx].horiz_center(), copy_cluster_list[dummy_idx].vert_center(), 0, 0.0) for dummy_idx in range(num_clusters)]
    for idx1 in range(num_iterations):
        old_clusters = list(new_clusters)
        new_clusters = [alg_cluster.Cluster(set([]), old_clusters[dummy_idx].horiz_center(), old_clusters[dummy_idx].vert_center(), 0, 0.0) for dummy_idx in range(num_clusters)]
        for idx2 in range(size):
            closest_idx = kmeans_closest_idx(cluster_list[idx2], old_clusters)
            new_clusters[closest_idx].merge_clusters(cluster_list[idx2])
    return new_clusters

def kmeans_closest_idx(cluster, clusters):
    """
    Helper function to compute the closest index of clusters with given cluster
    
    Input: Single cluster, Cluster list

    Output: Closest index
    """
    temp_dist = float("inf")
    idx = 0
    for dummy_idx in range(len(clusters)):
        dist = cluster.distance(clusters[dummy_idx])
        if dist < temp_dist:
            idx = dummy_idx
            temp_dist = dist
    return idx
