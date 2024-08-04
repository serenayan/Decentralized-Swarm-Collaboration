from drone import *

def test_grid_map():
    map = GridMap((9,9), (3,3))
    assert map.get_region(1,1) == (1,1)
    assert map.get_region(3,3) == (1,1)
    assert map.get_region(4,4) == (2,2)
    assert map.get_region(5,8) == (3,2)

def test_drone_visit_cells():
    drone = Drone(1, (9,9), (3,3))
    drone.map.visit_cell(1,3)
    region = drone.map.get_region(1,3)
    print(region)
    print(drone.map.region_exploration_score(*region))
    assert (drone.map.region_exploration_score(*region) == 1)
    drone.map.print()

if __name__ == "__main__":
    test_grid_map()
    test_drone_visit_cells()