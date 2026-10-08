from solvers.distance import build_distance_matrix, Coordinates, calculate_route_distance
from solvers.greedy import nearest_neighbour
from django.conf import settings
from infra.osrm import OSRMClient

def build_route(locations, start: int = 0) -> dict:
    coordinates = []
    for location in locations:
        coordinate = Coordinates(
            latitude=location["latitude"],
            longitude=location["longitude"],
        )

        coordinates.append(coordinate)
    osrm_client = OSRMClient(settings.OSRM_BASE_URL)
    distance_matrix = build_distance_matrix(coordinates)
    route = nearest_neighbour(distance_matrix, start)
    ordered_coordinates = [coordinates[index] for index in route]
    road_route = osrm_client.route(ordered_coordinates)
    total_distance = calculate_route_distance(route, distance_matrix)
    return {
    "route": route,
    "total_distance_km": road_route.distance_km,
    "duration_minutes": road_route.duration_minutes,
    "geometry": road_route.geometry,
}