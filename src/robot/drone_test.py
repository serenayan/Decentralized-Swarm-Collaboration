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

def test_message():
    state1 = State(1, Position(1,1), "Perception Context", "Inference Result")
    state2 = State(2, Position(1,1), "Perception Context 2", "Inference Result 2")
    message = Message()
    message.add_state(1, state1)
    message.add_state(2, state2)
    serialized_message = Message.serialize_to_string(message)
    serialized_deserialized_serialized_message = Message.serialize_to_string(Message.deserialize_from_string(Message.serialize_to_string(message)))
    assert serialized_message == serialized_deserialized_serialized_message

if __name__ == "__main__":
    test_grid_map()
    test_drone_visit_cells()
    test_message()