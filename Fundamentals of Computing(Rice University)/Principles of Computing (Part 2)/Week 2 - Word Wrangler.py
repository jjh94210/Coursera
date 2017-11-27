"""
Student code for Word Wrangler game
"""
# By Jaehwi Cho

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    original_list = list(list1)
    if original_list == []:
        return original_list
    no_duplicates = []
    dummy_index = 0
    while dummy_index < len(original_list) - 1:
        if original_list[dummy_index] != original_list[dummy_index + 1]:
            no_duplicates.append(original_list[dummy_index])
        dummy_index += 1
    no_duplicates.append(original_list[-1])
    return no_duplicates

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    intersect_list = []
    dummy_index_1 = 0
    dummy_index_2 = 0
    pivot = 0
    while dummy_index_2 < len(list2):
        dummy_index_1 = pivot
        while dummy_index_1 < len(list1):
            if list1[dummy_index_1] == list2[dummy_index_2]:
                intersect_list.append(list1[dummy_index_1])
                pivot = dummy_index_1 + 1
                break
            dummy_index_1 += 1
        dummy_index_2 += 1
    return intersect_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    merge_list = []
    temp1 = list(list1)
    temp2 = list(list2)
    while len(temp1) != 0 and len(temp2) != 0:
        if temp1[0] <= temp2[0]:
            merge_list.append(temp1.pop(0))
        else:
            merge_list.append(temp2.pop(0))
    if len(temp1) == 0:
        merge_list += temp2
    if len(temp2) == 0:
        merge_list += temp1
    return merge_list

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    temp1 = list(list1[:len(list1)/2])
    temp2 = list(list1[len(list1)/2:])
    return merge(merge_sort(temp1), merge_sort(temp2))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) < 1:
        return ['']
    first = word[:1]
    rest = word[1:]
    rest_strings = gen_all_strings(rest)
    for dummy_i in range(len(rest_strings)):
            for dummy_j in range(0, len(rest_strings[dummy_i]) + 1):
                rest_strings.append(rest_strings[dummy_i][:dummy_j] + first + rest_strings[dummy_i][dummy_j:])
    return rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    word_list = []
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    for line in netfile.readlines():
        word_list.append(line[:-1])
    return word_list

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates,
                                     intersect, merge_sort,
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

# http://www.codeskulptor.org/#user43_ud26soOHDUfUbEq.py
