"""
Merge function for 2048 game.
"""
# By Jaehwi Cho

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # Iterate over the input and create an output list
    # that has all of the non-zero tiles slid over 
    # to the beginning of the list 
    # with the appropriate number of zeroes at the end of the list
    list_output = list(line)
    for dummy_i in range(0, len(list_output)-1):
        if list_output[dummy_i] == 0:
            for dummy_j in range(dummy_i + 1, len(list_output)):
                if list_output[dummy_j] != 0:
                    list_output[dummy_i] = list_output[dummy_j]
                    list_output[dummy_j] = 0
                    break

    # Iterate over the list created in the previous step 
    # and create another new list in which pairs of tiles 
    # in the first list are replaced with a tile of twice the value and a zero tile.
    dummy_i = 0
    while dummy_i < (len(list_output) - 1):
        if list_output[dummy_i] == list_output[dummy_i + 1]:
            list_output[dummy_i] *= 2
            list_output[dummy_i + 1] = 0
            dummy_i += 2
        else:
            dummy_i += 1

    # Repeat step one using the list created in step two 
    # to slide the tiles to the beginning of the list again.
    for dummy_i in range(0, len(list_output)-1):
        if list_output[dummy_i] == 0:
            for dummy_j in range(dummy_i + 1, len(list_output)):
                if list_output[dummy_j] != 0:
                    list_output[dummy_i] = list_output[dummy_j]
                    list_output[dummy_j] = 0
                    break
    
    return list_output

# http://www.codeskulptor.org/#user43_IuY8AAH5kXJNN2H.py
