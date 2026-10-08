import pytest
from solvers.distance import Coordinates, build_distance_matrix, calculate_route_distance, haversine


def test_build_distance_matrix():
    coordinates = [
        Coordinates(latitude=6.5244, longitude=3.3792),
        Coordinates(latitude=6.6018, longitude=3.3515),
    ]

    matrix = build_distance_matrix(coordinates)

    assert len(matrix) == 2
    assert len(matrix[0]) == 2
    assert len(matrix[1]) == 2

    assert matrix[0][0] == 0
    assert matrix[1][1] == 0

    assert matrix[0][1] > 0
    assert matrix[0][1] == pytest.approx(matrix[1][0])


def test_haversine_same_coordinate():
    coordinate = Coordinates(
        latitude=6.5244,
        longitude=3.3792,
    )

    distance = haversine(coordinate, coordinate)

    assert distance == pytest.approx(0.0)


def test_haversine_between_two_coordinates():
    point_a = Coordinates(
        latitude=6.5244,
        longitude=3.3792,
    )

    point_b = Coordinates(
        latitude=6.6018,
        longitude=3.3515,
    )

    distance = haversine(point_a, point_b)

    assert distance == pytest.approx(9.12, rel=0.01)

def test_calculate_route_distance():
    matrix = [
        [0.0, 10.0, 15.0, 6.0],
        [10.0, 0.0, 8.0, 12.0],
        [15.0, 8.0, 0.0, 9.0],
        [6.0, 12.0, 9.0, 0.0],
    ]

    route = [0, 3, 2, 1]

    distance = calculate_route_distance(route, matrix)

    assert distance == pytest.approx(23.0)