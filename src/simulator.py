import matplotlib.pyplot as plt
import numpy as np
import random
from robot.drone import Drone

class Simulator:
    def __init__(self, map_size, num_drones):
        self.drones = [Drone(id=i, map_size=map_size) for i in range(num_drones)]
        for drone in self.drones:
            print(drone.get_position())

    def tick(self):
        for drone in self.drones:
            drone.move_randomly()
    
    def get_all_positions(self):
        return [drone.get_position() for drone in self.drones]

def update(simulator, scatter, texts):
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
        update(simulator, scatter, texts)

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
