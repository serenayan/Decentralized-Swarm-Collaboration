import matplotlib.pyplot as plt
import numpy as np
import random
from robot.drone import Drone
from scenario import SCENARIO_DICT

class Simulator:
    def __init__(self, map_size, region_dimensions, num_drones):
        self.drones = [Drone(id=i, region_dimensions=region_dimensions, map_size=map_size) for i in range(num_drones)]
        self.scenario_map = {}

        positions = random.sample([(x, y) for x in range(map_size) for y in range(map_size)], 2)
        (x1, y1), (x2, y2) = positions
        self.scenario_map[(x1, y1)] = SCENARIO_DICT["damaged_road_bridge"]
        self.scenario_map[(x2, y2)] = SCENARIO_DICT["trapped_person"]

        for drone in self.drones:
            print(drone.get_position())

    def tick(self):
        for drone in self.drones:
            drone.move()
            pos = drone.get_position()
            if pos in self.scenario_map:
                drone.add_to_current_perception_context([self.scenario_map[pos]])
            # drone.move_randomly()

        for drone in self.drones:
            broad_cast_lst = []
            for other_drone in self.drones:
                if done != other_drone and drone.can_communicate(other_drone, 3)
                    broad_cast_lst.append(other_drone)
            drone.set_neighbors(broad_cast_lst)

        for drone in self.drones:
            drone.update()
    
    def get_all_positions(self):
        return [drone.get_position() for drone in self.drones]

def tick_simulator(simulator, scatter, texts):
    simulator.tick()
    all_positions = simulator.get_all_positions()
    x_data = [pos.x for pos in all_positions]
    y_data = [pos.y for pos in all_positions]
    
    scatter.set_offsets(np.c_[x_data, y_data])
    
    for text, pos in zip(texts, all_positions):
        text.set_position((pos.x, pos.y))
    
    plt.draw()

def on_key_press(event, simulator, scatter, texts):
    if event.key == 'enter':
        tick_simulator(simulator, scatter, texts)

def main():
    map_dimensions = (9,9)  # Map size (9x9 grid)
    region_dimensions = (3,3)  # Region (3x3 grid)
    num_drones = 4  # Number of drones
    simulator = Simulator(map_size=map_dimensions, region_dimensions=region_dimensions, num_drones=num_drones)

    fig, ax = plt.subplots()
    ax.set_xlim(-0.5, n-0.5)
    ax.set_ylim(-0.5, n-0.5)

    # Initialize drones with dummy data to match the number of colors
    initial_positions = np.zeros((d, 2))
    colors = ['red', 'blue', 'green', 'purple']
    scatter = ax.scatter(initial_positions[:, 0], initial_positions[:, 1], c=colors[:d], s=100)
    texts = [ax.text(0, 0, str(i), fontsize=12, ha='center', va='center') for i in range(d)]

    # Draw grid
    ax.set_xticks(np.arange(0.5, n, 1), minor=False)
    ax.set_yticks(np.arange(0.5, n, 1), minor=False)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=0.5)

    # Connect the key press event
    fig.canvas.mpl_connect('key_press_event', lambda event: on_key_press(event, simulator, scatter, texts))

    plt.show()

if __name__ == "__main__":
    main()
