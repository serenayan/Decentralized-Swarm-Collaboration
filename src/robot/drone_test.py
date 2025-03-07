from drone import *

def test_grid_map():
    map = GridMap((9,9), (3,3))
    assert map.get_region(Position(1,1)) == (1,1)
    assert map.get_region(Position(3,3)) == (1,1)
    assert map.get_region(Position(4,4)) == (2,2)
    assert map.get_region(Position(5,8)) == (3,2)

    position = Position(1,3)
    map.visit_cell(position)
    region = map.get_region(position)
    assert (map.region_exploration_score(*region) == 1)
    map.print()

def test_drone_visit_cells():
    Drone(1, (9,9), (3,3))

def test_message():
    state1 = State(1, Position(1,1), "Perception Context", "Inference Result")
    state2 = State(2, Position(1,1), "Perception Context 2", "Inference Result 2")
    message = Message()
    message.add_state(1, state1)
    message.add_state(2, state2)
    serialized_message = Message.serialize_to_string(message)
    serialized_deserialized_serialized_message = Message.serialize_to_string(Message.deserialize_from_string(Message.serialize_to_string(message)))
    assert serialized_message == serialized_deserialized_serialized_message

def test_planner():
    event = Planner.execute_prompt("How many days are in a year?")
    print(str(event))

if __name__ == "__main__":
    test_grid_map()
    test_drone_visit_cells()
    test_message()
    test_planner()