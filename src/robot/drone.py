import numpy as np
from typing import List
import random

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"

class Drone():
    def __init__(self, id: int, map_size: int):
        self._id = id
        self._position = Position(random.randint(0, map_size - 1), random.randint(0, map_size - 1))
        self._map_size = map_size
        self._map = np.zeros((map_size, map_size), dtype=int)
        self._next_moves = []
        self._dwell_time = 0
        self._historical_perception_context = ""
        self._current_perception_context = []
        print(self._position.x, self._position.y)

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

    def move_randomly(self):
        direction = random.choice(['up', 'down', 'left', 'right'])
        
        if direction == 'up':
            self._position.y = (self._position.y + 1) % self._map_size
        elif direction == 'down':
            self._position.y = (self._position.y - 1) % self._map_size
        elif direction == 'left':
            self._position.x = (self._position.x - 1) % self._map_size
        elif direction == 'right':
            self._position.x = (self._position.x + 1) % self._map_size

    def __str__(self):
        return f"Drone(id={self.id}, position={self.position})"


if __name__ == "__main__":
    print("hello world")