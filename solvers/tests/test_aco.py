from solvers.aco import ant_colony


def test_ant_colony_finds_route():
    distance_matrix = [
        [0.0, 10.0, 15.0],
        [10.0, 0.0, 20.0],
        [15.0, 20.0, 0.0],
    ]

    route = ant_colony(distance_matrix, start=0)

    assert route[0] == 0
    assert set(route) == {0, 1, 2}
    assert len(route) == 3


def test_ant_colony_is_reproducible_with_seed():
    distance_matrix = [
        [0.0, 10.0, 15.0],
        [10.0, 0.0, 20.0],
        [15.0, 20.0, 0.0],
    ]

    route_1 = ant_colony(distance_matrix, start=0, seed=42)
    route_2 = ant_colony(distance_matrix, start=0, seed=42)

    assert route_1 == route_2