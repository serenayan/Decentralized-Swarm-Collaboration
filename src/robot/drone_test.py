import drone

def test_grid_map():
    map = drone.GridMap((9,9), (3,3))
    map.print()
    assert map.get_region(1,1) == (1,1)
    assert map.get_region(3,3) == (1,1)
    assert map.get_region(4,4) == (2,2)
    assert map.get_region(5,8) == (2,3)

if __name__ == "__main__":
    test_grid_map()