import math
import numpy as np
from typing import List
import random
from collections import namedtuple
import dataclasses
import json
import time

type DroneID = int
type PerceptionContext = str
type InferenceResult = str

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

@dataclasses.dataclass
class Position:
    x: int
    y: int

    def __str__(self):
        return f"({self.x}, {self.y})"

@dataclasses.dataclass
class State:
    id: DroneID
    position: Position
    perception_context: PerceptionContext
    inference_result: InferenceResult

class Message:
    def __init__(self):
        self._data : dict[DroneID, State] = {}

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def add_state(self, id: DroneID, state: State):
        assert id == state.id
        self._data[id] = state

    def get_state(self, id: DroneID):
        return self._data[id]
        
    @classmethod
    def serialize_to_string(cls, message) -> str:
        """Serializes the message to a json string."""
        return json.dumps(message.data, cls=EnhancedJSONEncoder)

    @classmethod
    def deserialize_from_string(cls, serialized_message: str):
        """Load a serialized message into a Message instance"""
        message = cls()
        # TODO: make this exception-safe
        message.data = json.loads(serialized_message)
        return message


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
    def __init__(self, id: DroneID, map_dimensions: tuple[int], region_dimensions: tuple[int]):
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
        self._current_perception_context = set() # Use set to easy dedup
        print(f"Initializing drone {self._id} at position {self._position.x, self._position.y}")

    @property
    def id(self) -> int:
        """Get the unique identifier for this drone."""
        return self._id
    
    @property
    def position(self) -> Position:
        """Get the position for this drone."""
        return self._position

    def move(self) -> None:
        """Move to the next position"""
        self.move_randomly()

    @property
    def map(self) -> Position:
        """Get the map for this drone."""
        return self._map

    def update(self) -> None:
        """
        Plans the next moves
        If current_perception_context, call LLM, delete current_perception_context
        Set historical_perception_context
        """
        if self._current_perception_context:
          self._current_perception_context = set()
          self._historical_perception_context = "updated history" + str(time.time())

    def can_communicate(self, other, threshold=3) -> bool:
        return (abs(self.position.x - other.position.x) < threshold) and (abs(self.position.y - other.position.y) < threshold)
    
    def set_neighbors(self, others) -> None:
        for other in others:
            other.add_to_current_perception_context(self._current_perception_context)

    def add_to_current_perception_context(self, perception_context: List[tuple]):
        self._current_perception_context.update(perception_context)

    def move_randomly(self):
        # Get current position
        x, y = self._position.x, self._position.y
        max_x, max_y = self._map_dimensions

        # Determine possible directions based on current position
        possible_directions = []
        if y < max_y - 1:
            possible_directions.append('up')
        if y > 0:
            possible_directions.append('down')
        if x > 0:
            possible_directions.append('left')
        if x < max_x - 1:
            possible_directions.append('right')

        # Choose a direction randomly from possible directions
        direction = random.choice(possible_directions)

        # Move the drone in the chosen direction
        if direction == 'up':
            self._position.y += 1
        elif direction == 'down':
            self._position.y -= 1
        elif direction == 'left':
            self._position.x -= 1
        elif direction == 'right':
            self._position.x += 1

    def __str__(self):
        return f"Drone(id={self.id}, position={self.position})"


if __name__ == "__main__":
    drone = Drone(1, (9,9), (3,3))