import numpy as np
from typing import List

class Position:
     def __init__(self, x, y):
         self.x = x
         self.y =y

class Drone():
    def __init__(self, id: int, x: int, y: int):
        self._id = None
        self._position = Position(x,y)
        self._map = np.zeros(3,3,dtype=int)
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
    print("hello world")