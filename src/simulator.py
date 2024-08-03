import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

class Drone:
    def __init__(self, map_size, id):
        self.map_size = map_size
        self.id = id
        self.position = [random.randint(0, map_size - 1), random.randint(0, map_size - 1)]

    def move_randomly(self):
        # Move randomly within the bounds of the map
        self.position[0] = (self.position[0] + random.choice([-1, 0, 1])) % self.map_size
        self.position[1] = (self.position[1] + random.choice([-1, 0, 1])) % self.map_size

    def get_position(self):
        return self.position

class Simulator:
    def __init__(self, map_size, num_drones):
        self.drones = [Drone(map_size=map_size, id=i) for i in range(num_drones)]

    def tick(self):
        for drone in self.drones:
            drone.move_randomly()
    
    def get_all_positions(self):
        return [drone.get_position() for drone in self.drones]

def update(frame, simulator, scatter, texts):
    simulator.tick()
    all_positions = simulator.get_all_positions()
    x_data = [pos[0] for pos in all_positions]
    y_data = [pos[1] for pos in all_positions]
    
    scatter.set_offsets(np.c_[x_data, y_data])
    
    for text, pos in zip(texts, all_positions):
        text.set_position((pos[0], pos[1]))
    
    return scatter, *texts

def main():
    n = 9  # Map size (9x9 grid)
    d = 4  # Number of drones
    simulator = Simulator(map_size=n, num_drones=d)

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

    ani = animation.FuncAnimation(fig, update, fargs=(simulator, scatter, texts), frames=360, interval=500, blit=True)
    plt.show()

if __name__ == "__main__":
    main()
