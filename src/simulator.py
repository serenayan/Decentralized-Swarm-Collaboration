import matplotlib.pyplot as plt
import numpy as np
import random
from robot.drone import Drone
from scenario import SCENARIO_DICT

class Simulator:
    def __init__(self, map_dimensions, region_dimensions, num_drones):
        self.drones = [Drone(id=i, map_dimensions=map_dimensions, region_dimensions=region_dimensions) for i in range(num_drones)]
        self.scenario_map = {}

        positions = random.sample([(x, y) for x in range(map_dimensions[0]) for y in range(map_dimensions[1])], 2)
        (x1, y1), (x2, y2) = positions
        self.scenario_map[(x1, y1)] = SCENARIO_DICT["damaged_road_bridge"]
        self.scenario_map[(x2, y2)] = SCENARIO_DICT["trapped_person"]

        for drone in self.drones:
            print(drone.position)

        self.arrows = []

    def clear_arrows(self, ax):
        for arrow in self.arrows:
            arrow.remove()
        self.arrows = []
        plt.draw()

    def tick(self, ax):
        self.clear_arrows(ax)
        
        for drone in self.drones:
            drone.move()
            pos = drone.position
            if pos in self.scenario_map:
                drone.add_to_current_perception_context([(drone.id(), self.scenario_map[pos])])

        for drone in self.drones:
            broad_cast_lst = []
            for other_drone in self.drones:
                if drone != other_drone and drone.can_communicate(other_drone, 4):
                    broad_cast_lst.append(other_drone)
            
            # Draw arrows for broadcasting information
            for neighbor in broad_cast_lst:
                arrow = ax.annotate(
                    '', xy=(neighbor.position.x, neighbor.position.y), xytext=(drone.position.x, drone.position.y),
                    arrowprops=dict(arrowstyle="->", color='blue')
                )
                self.arrows.append(arrow)
                
            drone.set_neighbors(broad_cast_lst)

        for drone in self.drones:
            drone.update()
    
    def get_all_positions(self):
        return [drone.position for drone in self.drones]

def tick_simulator(simulator, scatter, texts, ax):
    simulator.tick(ax)
    all_positions = simulator.get_all_positions()
    x_data = [pos.x for pos in all_positions]
    y_data = [pos.y for pos in all_positions]
    
    scatter.set_offsets(np.c_[x_data, y_data])
    
    for text, pos in zip(texts, all_positions):
        text.set_position((pos.x, pos.y))
    
    plt.draw()

def on_key_press(event, simulator, scatter, texts, ax):
    if event.key == 'enter':
        tick_simulator(simulator, scatter, texts, ax)

def main():
    map_dimensions = (9,9)  # Map size (9x9 grid)
    region_dimensions = (3,3)  # Region (3x3 grid)
    num_drones = 4  # Number of drones
    simulator = Simulator(map_dimensions=map_dimensions, region_dimensions=region_dimensions, num_drones=num_drones)

    fig, ax = plt.subplots()
    ax.set_xlim(-0.5, map_dimensions[0]-0.5)
    ax.set_ylim(-0.5, map_dimensions[1]-0.5)

    # Initialize drones with dummy data to match the number of colors
    initial_positions = np.zeros((num_drones, 2))
    colors = ['red', 'blue', 'green', 'purple']
    scatter = ax.scatter(initial_positions[:, 0], initial_positions[:, 1], c=colors[:num_drones], s=100)
    texts = [ax.text(0, 0, str(i), fontsize=12, ha='center', va='center') for i in range(num_drones)]

    # Draw grid
    ax.set_xticks(np.arange(0.5, map_dimensions[0], 1), minor=False)
    ax.set_yticks(np.arange(0.5, map_dimensions[1], 1), minor=False)
    ax.grid(which='major', color='gray', linestyle='--', linewidth=0.5)

    # Connect the key press event
    fig.canvas.mpl_connect('key_press_event', lambda event: on_key_press(event, simulator, scatter, texts, ax))

    plt.show()

if __name__ == "__main__":
    main()
