import math
import numpy as np
import random
import dataclasses
import json
# from planner import Planner
from typing import List
import replicate

class Planner:
    @staticmethod
    def execute_prompt(prompt: str) -> str:
        input = {
            "prompt": prompt,
            "max_tokens": 1024
        }
        result = ""
        for event in replicate.stream(
            "meta/meta-llama-3.1-405b-instruct",
            input=input
        ):
            result += str(event)
        return result

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

    def empty(self):
        return len(self.data.keys()) == 0

    def clear(self):
        self.data.clear()

    def copy(self, other):
        """Replace the data with other data"""
        self.data = other.data.copy()

    def update(self, other):
        """Update the data with other data"""
        for id, state in other.data.items():
            self.data[id] = state

    def add_state(self, id: DroneID, state: State):
        assert id == state.id
        self.data[id] = state

    def get_state(self, id: DroneID):
        return self.data[id]

    def get_prompt(self, id: DroneID):
        prompt = ""
        if id in self.data.keys():
             prompt += f"Our drone has observed that {self.data[id].perception_context}"
        if self.data:
            prompt = "Our drone knows some information from its peers. "
            for id, state in self.data.items():
                prompt += f"peer {id} has observed that {state.perception_context}."
                if state.inference_result:
                    prompt += f"peer {id} has planned the following response: {state.inference_result}"
        return prompt
        
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
        self._map_dimensions = map_dimensions
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

    @property
    def map_dimensions(self):
        return self._map_dimensions

    @property
    def region_dimensions(self):
        return self._region_dimensions

    def get_region(self, position: Position) -> tuple[int]:
        """ Gets the region index of a position. """
        return (math.ceil(position.y / self._region_dimensions[0]), math.ceil(position.x / self._region_dimensions[1]))

    def visit_cell(self, position: Position):
        """ Increment the counter for the cell. """
        self._map[position.y][position.x] += 1

    def region_exploration_score(self, region_j, region_i):
        """ How many times we have visited cells in a region """
        # Probably more efficient to represent a 2d array of regions, and a region is a datastructure containing a 2d array of cells.
        score = 0
        for y, x in np.ndindex(self._map.shape):
            if self.get_region(Position(x,y)) == (region_i, region_j):
                score += self._map[y][x]
        return score

    def get_position_of_least_visited_cell_in_region(self, region: tuple[int]) -> Position:
        position = None
        least_visitation = 1000
        for y, x in np.ndindex(self._map.shape):
            if self.get_region(Position(x,y)) == region and self._map[y][x] < least_visitation:
                position = Position(x,y)
        return position

class Drone():
    def __init__(self, id: DroneID, map_dimensions: tuple[int], region_dimensions: tuple[int]):
        # Sanitization
        assert map_dimensions[0] > 0 and map_dimensions[1] > 0
        assert region_dimensions[0] > 0 and region_dimensions[1] > 0
        # Initialize
        self._id = id
        self._position = Position(random.randint(0, map_dimensions[0] - 1), random.randint(0, region_dimensions[1] - 1))
        self._map_dimensions = map_dimensions
        self._region_dimensions = region_dimensions
        self._map = GridMap(map_dimensions, region_dimensions)
        self._planned_moves: List[Position] = [] # A list of destinations
        self._dwell_time = 0
        self._historical_data: Message = Message()
        self._current_data: Message = Message()
        print(f"Initializing drone {self._id} at position {self._position.x, self._position.y}")

    @property
    def id(self) -> int:
        """Get the unique identifier for this drone."""
        return self._id
    
    @property
    def position(self) -> Position:
        """Position for this drone."""
        return self._position

    @property
    def map(self) -> Position:
        """Map for this drone."""
        return self._map

    @property
    def historical_data(self) -> Message:
        """Historical data for this drone."""
        return self._historical_data

    @property
    def current_data(self) -> Message:
        """Current data for this drone."""
        return self._current_data

    def move(self) -> None:
        """Move to the next position"""
        # Use planned moves if they exist.
        planned_moves_count = len(self._planned_moves)
        if planned_moves_count > 0:
            next_target_position = self._planned_moves[0]
            self.move_toward_target(next_target_position)
            if self.position == next_target_position:
                del self._planned_moves[0]
                assert len(self._planned_moves) < planned_moves_count

        # Otherwise, move randomly.
        self.move_randomly()
        self._map.visit_cell(self.position)

    def update(self) -> None:
        """
        Plans the next moves
        If current_data, call LLM, delete current_data
        Set historical_data
        """
        if not self.current_data.empty():
            if self.id in self.current_data.data.keys():
                state = self.current_data.data[self.id]
                prompt = f"Our drone is on a {self._map_dimensions} by {self._map_dimensions} grid of cells. The map is also divided into a {self._region_dimensions} by {self._region_dimensions} grid of regions. Each cell is contained in a region."
                prompt += "If all else is equal, we prefer to move toward the region with the least exploration. "
                prompt += "Historically, old information is that "
                prompt += self.historical_data.get_prompt(self.id)
                prompt += "Currently, more recent information is available."
                prompt += self.current_data.get_prompt(self.id)
                prompt += " Given this information, should the drone move to the region up, down, left, or right?"
                state.inference_result = Planner.execute_prompt(prompt)
                target_position = self.get_target_position_from_interfence_result(state.inference_result)
                if target_position is not None:
                    # TODO: Currently, we only support a single target position in the planned moves.
                    self._planned_moves = [target_position]
            self.historical_data.copy(self.current_data)
            self.current_data.clear()
            assert not self.historical_data.empty()

    def can_communicate(self, other, threshold=3) -> bool:
        return (abs(self.position.x - other.position.x) < threshold) and (abs(self.position.y - other.position.y) < threshold)
    
    def set_neighbors(self, others) -> None:
        """Broadcasts this Drone's state to all the neighboring drones so that we synchronize state."""
        if self.current_data:
            for other in others:
                other.update_current_data(self.current_data)

    def update_current_data(self, message: Message):
        """Update this drone's current data with data from other drones."""
        self.current_data.update(message)

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

    def move_toward_target(self, target: Position):
        # Newton's method, simple shortest path.
        grad_x = target.x - self._position.x
        grad_y = target.y - self._position.y
        if grad_x > grad_y:
            self._position.x += int(grad_x/abs(grad_x))
        else:
            self._position.y += int(grad_y/abs(grad_y))

    def get_target_position_from_interfence_result(self, inference_result: InferenceResult) -> Position | None:
        target_position = None
        current_region = self.map.get_region(self.position)
        target_region = current_region
        if "up" in inference_result or "Up" in inference_result:
            target_region = (current_region[0]+1, current_region[1])
            target_position = self.map.get_position_of_least_visited_cell_in_region(target_region)
        elif "down" in inference_result or "Down" in inference_result:
            target_region = (current_region[0]-1, current_region[1])
            target_position = self.map.get_position_of_least_visited_cell_in_region(target_region)
        if "right" in inference_result or "Right" in inference_result:
            target_region = (current_region[0], current_region[1]+1)
            target_position = self.map.get_position_of_least_visited_cell_in_region(target_region)
        elif "left" in inference_result or "Left" in inference_result:
            target_region = (current_region[0], current_region[1]-1)
            target_position = self.map.get_position_of_least_visited_cell_in_region(target_region)

        return target_position

    def __str__(self):
        return f"Drone(id={self.id}, position={self.position})"


if __name__ == "__main__":
    drone = Drone(1, (9,9), (3,3))