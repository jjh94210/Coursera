"""
Student portion of Zombie Apocalypse mini-project
"""
# By Jaehwi Cho

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None,
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for dummy_zombie in self._zombie_list:
            yield dummy_zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for dummy_human in self._human_list:
            yield dummy_human

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        grid_height = self.get_grid_height()
        grid_width = self.get_grid_width()
        visited = poc_grid.Grid(grid_height, grid_width)
        distance_field = [[grid_height * grid_width for dummy_col in range(grid_width)]
                          for dummy_row in range(grid_height)]
        boundary = poc_queue.Queue()

        if entity_type == ZOMBIE:
            for dummy_type in self._zombie_list:
                boundary.enqueue(dummy_type)
        elif entity_type == HUMAN:
            for dummy_type in self._human_list:
                boundary.enqueue(dummy_type)

        for dummy_type in boundary:
            visited.set_full(dummy_type[0], dummy_type[1])
            distance_field[dummy_type[0]][dummy_type[1]] = 0
        while len(boundary) != 0:
            current_cell = boundary.dequeue()
            neighbor_cell_list = visited.four_neighbors(current_cell[0], current_cell[1])
            for neighbor_cell in neighbor_cell_list:
                if visited.is_empty(neighbor_cell[0], neighbor_cell[1]) and self.is_empty(neighbor_cell[0], neighbor_cell[1]):
                    visited.set_full(neighbor_cell[0], neighbor_cell[1])
                    boundary.enqueue(neighbor_cell)
                    distance_field[neighbor_cell[0]][neighbor_cell[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
        return distance_field

    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        final_human_list = []
        for dummy_human in self._human_list:
            boundary_list = self.eight_neighbors(dummy_human[0], dummy_human[1])
            boundary_list.append(dummy_human)
            distance_list = []
            for dummy_boundary in boundary_list:
                if self.is_empty(dummy_boundary[0], dummy_boundary[1]):
                    distance_list.append(zombie_distance_field[dummy_boundary[0]][dummy_boundary[1]])
            move_list = []
            for dummy_boundary in boundary_list:
                if zombie_distance_field[dummy_boundary[0]][dummy_boundary[1]] == max(distance_list) and self.is_empty(dummy_boundary[0], dummy_boundary[1]):
                    move_list.append(dummy_boundary)
            final_human_list.append(move_list[random.randrange(0, len(move_list))])
        self._human_list = final_human_list

    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        final_zombie_list = []
        for dummy_zombie in self._zombie_list:
            boundary_list = self.four_neighbors(dummy_zombie[0], dummy_zombie[1])
            boundary_list.append(dummy_zombie)
            distance_list = []
            for dummy_boundary in boundary_list:
                if self.is_empty(dummy_boundary[0], dummy_boundary[1]):
                    distance_list.append(human_distance_field[dummy_boundary[0]][dummy_boundary[1]])
            move_list = []
            for dummy_boundary in boundary_list:
                if human_distance_field[dummy_boundary[0]][dummy_boundary[1]] == min(distance_list) and self.is_empty(dummy_boundary[0], dummy_boundary[1]):
                    move_list.append(dummy_boundary)
            final_zombie_list.append(move_list[random.randrange(0, len(move_list))])
        self._zombie_list = final_zombie_list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))

# http://www.codeskulptor.org/#user43_mkuf2tQdx3EdWjn.py
