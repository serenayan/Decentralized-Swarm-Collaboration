import math
import numpy as np
from typing import List

class Position:
     def __init__(self, x, y):
         self.x = x
         self.y = y

class GridMap:
    def __init__(self, dimensions: tuple[int], region_dimensions: tuple[int]):
        assert len(dimensions) == 2, "Need to specify 2 dimensions."
        assert region_dimensions[0] < dimensions[0] and region_dimensions[1] < dimensions[1]
        self._dimensions = dimensions
        self._region_dimensions = region_dimensions
        self._grid = np.zeros((9,9),dtype=int)
    
    def print(self):
        """
        Prints 9x9 numpy array input board in an easier to read format.
        """
        
        # Some basic checks
        assert self._grid.shape == (9, 9)
        assert type(self._grid) == np.ndarray
        
        # Convert array elements to strings
        board_str = self._grid.astype(str)
        
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

    def get_region(self, i: int, j: int) -> tuple[int]:
        return (math.ceil(i / self._region_dimensions[0]), math.ceil(j / self._region_dimensions[1]))

class Drone():
    def __init__(self, id: int, x: int, y: int):
        self._id = None
        self._position = Position(x,y)
        self._map = np.zeros(9,9,dtype=int)
        self._next_moves = []
        self._dwell_time = 0
        self._historical_perception_context = ""
        self._current_perception_context = []

    def get_id(self) -> int:
        """Get the unique identifier for this drone."""
        return self._id
    
    def get_position(self) -> Position:
        """Get the position for this drone."""
        return self._position

    def update(self) -> None:
        """Plans the next moves"""
        return

    def can_communicate(self) -> bool:
        return True
    
    def set_neighbors(self) -> None:
        return

    def add_to_current_perception_context(self, perception_context: List[str]):
        return


if __name__ == "__main__":
    map = GridMap((9,9), (3,3))
    map.print()
    print(map.get_region(1,1))
    print(map.get_region(3,3))
    print(map.get_region(4,4))
    print("hello world")