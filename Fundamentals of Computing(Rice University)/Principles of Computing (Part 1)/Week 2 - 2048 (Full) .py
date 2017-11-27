"""
Clone of 2048 game.
"""
# By Jaehwi Cho

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
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

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._tiles_height = grid_height
        self._tiles_width = grid_width
        self.reset()
        self._initial_tiles = {UP:[], DOWN:[], LEFT:[], RIGHT:[]}
        for dummy_col in range(self.get_grid_width()):
            self._initial_tiles[UP].append((0, dummy_col))
            self._initial_tiles[DOWN].append((self.get_grid_height() - 1, dummy_col))
        for dummy_row in range(self.get_grid_height()):
            self._initial_tiles[LEFT].append((dummy_row, 0))
            self._initial_tiles[RIGHT].append((dummy_row, self.get_grid_width() - 1))

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._tiles = [[0 for dummy_col in range(self.get_grid_width())]
                         for dummy_row in range(self.get_grid_height())]
        for dummy_num in range(2):
            self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        debugging_message = "Current tile numbers are \n"
        for dummy_col in range(self.get_grid_width()):
            debugging_message += " ---"
        debugging_message += " \n"
        for dummy_row in range(self.get_grid_height()):
            debugging_message += "| "
            for dummy_col in range(self.get_grid_width()):
                debugging_message += (str(self._tiles[dummy_row][dummy_col]) + " | ")
            debugging_message += " \n"
            for dummy_col in range(self.get_grid_width()):
                debugging_message += " ---"
            debugging_message += " \n"
        return debugging_message

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._tiles_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._tiles_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        is_equal = True
        for dummy_tile in self._initial_tiles[direction]:
            temporary_list = []
            for dummy_num in range(len(self._initial_tiles[(direction + 1) % 4 + 1])):
                temporary_list.append(self._tiles[dummy_tile[0] + dummy_num * OFFSETS[direction][0]][dummy_tile[1] + dummy_num * OFFSETS[direction][1]])
            if(temporary_list != merge(temporary_list)):
                temporary_list = merge(temporary_list)
                for dummy_num in range(len(self._initial_tiles[(direction + 1) % 4 + 1])):
                    self._tiles[dummy_tile[0] + dummy_num * OFFSETS[direction][0]][dummy_tile[1] + dummy_num * OFFSETS[direction][1]] = temporary_list[dummy_num]
                is_equal = False
        if not is_equal:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        is_empty = False
        while(not is_empty):
            dummy_random_row = random.randrange(0, self._tiles_height)
            dummy_random_col = random.randrange(0, self._tiles_width)
            if self.get_tile(dummy_random_row, dummy_random_col) == 0:
                is_empty = True
        dummy_probability = random.random()
        if dummy_probability < 0.9:
            self.set_tile(dummy_random_row, dummy_random_col, 2)
        else:
            self.set_tile(dummy_random_row, dummy_random_col, 4)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._tiles[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._tiles[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

# http://www.codeskulptor.org/#user43_b3yRjT5EzYaR3dP.py
