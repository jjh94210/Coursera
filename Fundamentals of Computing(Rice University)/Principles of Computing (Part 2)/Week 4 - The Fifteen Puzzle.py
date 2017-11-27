"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""
# By Jaehwi Cho

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        if self._grid[target_row][target_col] != 0:
            return False
        given_pos_val = target_col + target_row * self._width
        end_pos_val = self._width * self._height - 1
        for dummy_val in range(given_pos_val + 1, end_pos_val + 1):
            dummy_col = dummy_val % self._width
            dummy_row = (dummy_val - dummy_col) / self._width
            if self._grid[dummy_row][dummy_col] != dummy_val:
                return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.lower_row_invariant(target_row, target_col)
        move_string = ""
        current_target_pos = self.current_position(target_row, target_col)
        if (target_row - 1, target_col) == current_target_pos:
            move_string += "uld"
            self.update_puzzle(move_string)
            assert self.lower_row_invariant(target_row, target_col - 1)
            return move_string
        row_dist = target_row - current_target_pos[0]
        col_dist = target_col - current_target_pos[1]
        # check cyclic move direction
        clockwise = True
        if row_dist == 0:
            move_string += (col_dist * "l" + "u" + col_dist * "r" + "d") \
                           * (col_dist - 1)
            move_string += "l"
        else:
            move_string += "u"
            if col_dist < 0:
                clockwise = False
                col_dist *= (-1)
            if row_dist == 1:
                if clockwise:
                    move_string += (col_dist * "l" + "u" + col_dist * "r" + "d") \
                                   * (col_dist)
                else:
                    move_string += (col_dist * "r" + "u" + col_dist * "l" + "d") \
                                   * (col_dist)
            else:
                row_dist -= 1
                if clockwise:
                    if col_dist == 0:
                        col_dist = 1
                        cycle = row_dist - 1
                    else:
                        cycle = row_dist + col_dist - 1
                    move_string += (row_dist * "u" + col_dist * "l" + row_dist * "d" + col_dist * "r") \
                                   * cycle
                else:
                    move_string += (row_dist * "u" + col_dist * "r" + row_dist * "d" + col_dist * "l") \
                                   * (row_dist + col_dist - 1)
            move_string += "ulddruld"
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row, target_col - 1)
        return move_string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.lower_row_invariant(target_row, 0)
        move_string = ""
        current_target_pos = self.current_position(target_row, 0)
        if (target_row - 1, 0) == current_target_pos:
            move_string += ("u" + (self._width - 1) * "r")
            self.update_puzzle(move_string)
            assert self.lower_row_invariant(target_row - 1, self._width - 1)
            return move_string
        row_dist = target_row - current_target_pos[0]
        col_dist = current_target_pos[1]
        move_string += "u"
        if row_dist == 1:
            move_string += (col_dist * "r" + "u" + col_dist * "l" + "d") \
                           * (col_dist - 1)
        else:
            row_dist -= 1
            if col_dist == 0:
                col_dist = 1
                cycle = row_dist + col_dist
            else:
                cycle = row_dist + col_dist - 1
            move_string += (col_dist * "r" + row_dist * "u" + col_dist * "l" + row_dist * "d") \
                           * cycle
        move_string += "ruldrdlurdluurddlu"
        move_string += (self._width - 1) * "r"
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row - 1, self._width - 1)
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self._grid[0][target_col] != 0:
            return False
        if self.current_position(1, target_col) != (1, target_col):
            return False
        for dummy_row in range(2):
            for dummy_col in range(target_col + 1, self._width):
                if self.current_position(dummy_row, dummy_col) != (dummy_row, dummy_col):
                    return False
        for dummy_row in range(2, self._height):
            for dummy_col in range(0, self._width):
                if self.current_position(dummy_row, dummy_col) != (dummy_row, dummy_col):
                    return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        # to check two right row of empty space
        if self._grid[1][target_col] != 0:
            return False
        for dummy_row in range(2):
            for dummy_col in range(target_col + 1, self._width):
                if self.current_position(dummy_row, dummy_col) != (dummy_row, dummy_col):
                    return False
        for dummy_row in range(2, self._height):
            for dummy_col in range(0, self._width):
                if self.current_position(dummy_row, dummy_col) != (dummy_row, dummy_col):
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.row0_invariant(target_col)
        move_string = ""
        current_target_pos = self.current_position(0, target_col)
        if current_target_pos == (0, target_col - 1):
            move_string += "ld"
            self.update_puzzle(move_string)
            assert self.row1_invariant(target_col - 1)
            return move_string
        if current_target_pos == (1, target_col - 1):
            move_string += "lldurdlurrdluldrruld"
            self.update_puzzle(move_string)
            assert self.row1_invariant(target_col - 1)
            return move_string
        move_string += "ld"
        row_dist = current_target_pos[0]
        col_dist = target_col - current_target_pos[1] - 1
        clockwise = True
        if row_dist == 0:
            clockwise = False
        if clockwise:
            move_string += (col_dist * "l" + "u" + col_dist * "r" + "d") \
                           * (col_dist - 1)
            move_string += "l"
        else:
            move_string += ("u" + col_dist * "l" + "d" + col_dist * "r") \
                           * (col_dist)
            move_string += "uld"
        move_string += "urdlurrdluldrruld"
        self.update_puzzle(move_string)
        assert self.row1_invariant(target_col - 1)
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.row1_invariant(target_col)
        move_string = ""
        current_target_pos = self.current_position(1, target_col)
        if current_target_pos == (0, target_col):
            move_string += "u"
            self.update_puzzle(move_string)
            assert self.row0_invariant(target_col)
            return move_string
        if current_target_pos == (1, target_col - 1):
            move_string += "lur"
            self.update_puzzle(move_string)
            assert self.row0_invariant(target_col)
            return move_string
        row_dist = current_target_pos[0]
        col_dist = target_col - current_target_pos[1]
        clockwise = True
        if row_dist == 0:
            clockwise = False
        if clockwise:
            move_string += (col_dist * "l" + "u" + col_dist * "r" + "d") \
                           * (col_dist - 1)
            move_string += "lur"
        else:
            move_string += ("u" + col_dist * "l" + "d" + col_dist * "r") \
                           * (col_dist)
            move_string += "u"
        self.update_puzzle(move_string)
        assert self.row0_invariant(target_col)
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        assert self.row1_invariant(1)
        zero_pos = self.current_position(0, 0)
        move_string = zero_pos[1] * "l" + zero_pos[0] * "u"
        pos_1_num = self.get_number(0, 1)
        if pos_1_num == self._width:
            move_string += "rdlu"
        elif pos_1_num == self._width + 1:
            move_string += "drul"
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(0, 0)
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        zero_pos = self.current_position(0, 0)
        height = self._height
        width = self._width
        move_string = (height - zero_pos[0] - 1) * "d" + (width - zero_pos[1] - 1) * "r"
        self.update_puzzle(move_string)
        # phase 1
        for dummy_row in range(height - 1, 1, -1):
            for dummy_col in range(width - 1, 0, -1):
                move_string += self.solve_interior_tile(dummy_row, dummy_col)
            move_string += self.solve_col0_tile(dummy_row)
        # phase 2
        for dummy_index in range(width - 1, 1, -1):
            assert self.row1_invariant(dummy_index)
            move_string += self.solve_row1_tile(dummy_index)
            assert self.row0_invariant(dummy_index)
            move_string += self.solve_row0_tile(dummy_index)
        # phase 3
        move_string += self.solve_2x2()
        return move_string

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

# http://www.codeskulptor.org/#user43_jwBoLJil3yK1zOW.py
