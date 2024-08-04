import math
import numpy as np
from typing import List
import random

class Position:
    def __init__(self, x, y):
         self.x = x
         self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"

class GridMap:
    def __init__(self, map_dimensions: tuple[int], region_dimensions: tuple[int]):
        assert len(map_dimensions) == 2, "Need to specify 2 dimensions."
        assert region_dimensions[0] < map_dimensions[0] and region_dimensions[1] < map_dimensions[1]
        self._dimensions = map_dimensions
        self._region_dimensions = region_dimensions
        self._map = np.zeros((9,9),dtype=int)
    
    def print(self):
        """
        Prints 9x9 numpy array input board in an easier to read format.
        """
        
        # Some basic checks
        assert self._map.shape == (9, 9)
        assert type(self._map) == np.ndarray
        
        # Convert array elements to strings
        board_str = self._map.astype(str)
        
        # Our row separator
        row_sep = '-'*25

        # Loop through 9 rows
        for i in range(9):
            
            # At each multiple of 3, print row separator
            if i % 3 == 0:
                print(row_sep)

            # Get row data
            row = board_str[i]

            # Format row of data with pipe separators at each end, and between each sub grid
            print('| '+' '.join(row[0:3])+' | '+' '.join(row[3:6])+' | '+' '.join(row[6:])+' |')

        # Print final row separator at bottom after loops finish
        print(row_sep)

    def get_region(self, j: int, i: int) -> tuple[int]:
        """ Gets the region index. """
        return (math.ceil(i / self._region_dimensions[0]), math.ceil(j / self._region_dimensions[1]))

    def visit_cell(self, j : int, i: int):
        """ Increment the counter for the cell. """
        self._map[i][j] += 1

    def region_exploration_score(self, region_j, region_i):
        """ How many times we have visited cells in a region """
        # Probably more efficient to represent a 2d array of regions, and a region is a datastructure containing a 2d array of cells.
        score = 0
        for i, j in np.ndindex(self._map.shape):
            if self.get_region(i,j) == (region_i, region_j):
                score += self._map[i][j]
        return score

class Drone():
    def __init__(self, id: int, map_dimensions: tuple[int], region_dimensions: tuple[int]):
        # Sanitization
        assert map_dimensions[0] > 0 and map_dimensions[1] > 0
        assert region_dimensions[0] > 0 and region_dimensions[1] > 0
        # Initialize
        self._id = id
        self._position = Position(random.randint(0, map_dimensions[0] - 1), random.randint(0, region_dimensions[1] - 1))
        self._map_dimensions = map_dimensions
        self._map = GridMap(map_dimensions, region_dimensions)
        self._next_moves = []
        self._dwell_time = 0
        self._historical_perception_context = ""
        self._current_perception_context = []
        print(f"Initializing drone {self._id} at position {self._position.x, self._position.y}")

    @property
    def id(self) -> int:
        """Get the unique identifier for this drone."""
        return self._id
    
    @property
    def position(self) -> Position:
        """Get the position for this drone."""
        return self._position

    @property
    def map(self) -> Position:
        """Get the map for this drone."""
        return self._map

    def update(self) -> None:
        """Plans the next moves"""
        return

    def can_communicate(self) -> bool:
        return True
    
    def set_neighbors(self) -> None:
        return

    def add_to_current_perception_context(self, perception_context: List[str]):
        return

    def move_randomly(self):
        # TODO: account for edge cases and knowledge of previously explored regions.
        direction = random.choice(['up', 'down', 'left', 'right'])
        
        if direction == 'up':
            self._position.y = (self._position.y + 1) % self._map_dimensions[1]
        elif direction == 'down':
            self._position.y = (self._position.y - 1) % self._map_dimensions[1]
        elif direction == 'left':
            self._position.x = (self._position.x - 1) % self._map_dimensions[0]
        elif direction == 'right':
            self._position.x = (self._position.x + 1) % self._map_dimensions[0]

    def __str__(self):
        return f"Drone(id={self.id}, position={self.position})"


if __name__ == "__main__":
    drone = Drone(1, (9,9), (3,3))