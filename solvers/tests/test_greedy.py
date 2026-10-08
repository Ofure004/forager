from solvers.greedy import nearest_neighbour


def test_nearest_neighbour():
    matrix = [
        [0.0, 10.0, 15.0, 6.0],
        [10.0, 0.0, 8.0, 12.0],
        [15.0, 8.0, 0.0, 9.0],
        [6.0, 12.0, 9.0, 0.0],
    ]

    route = nearest_neighbour(matrix, start=0)

    assert route == [0, 3, 2, 1]