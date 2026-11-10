from solvers.distance import Coordinates
from solvers.osrm import osrm_distance_matrix


def test_osrm_distance_matrix():
    locations = [
        Coordinates(latitude=6.5244, longitude=3.3792),
        Coordinates(latitude=6.4281, longitude=3.4484),
        Coordinates(latitude=6.4378, longitude=3.4211),
    ]

    matrix = osrm_distance_matrix(locations)

    assert len(matrix) == 3
    assert all(len(row) == 3 for row in matrix)

    for i in range(3):
        assert matrix[i][i] == 0

    assert all(
        distance >= 0
        for row in matrix
        for distance in row
    )