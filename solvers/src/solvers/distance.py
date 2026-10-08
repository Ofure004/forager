from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Coordinates:
    latitude: float
    longitude: float

def radianconverter(degree:float) -> float:
    radian = degree * (math.pi / 180)
    return radian

def haversine(coord1: Coordinates, coord2:Coordinates) -> float : 
    lat1 = radianconverter(coord1.latitude)
    lat2 = radianconverter(coord2.latitude)
    long1 = radianconverter(coord1.longitude)
    long2 = radianconverter(coord2.longitude)

    latdifference = lat1 - lat2
    longdifference = long1 - long2

    a = math.sin(latdifference / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(longdifference / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = 6371 * c
    return distance

def build_distance_matrix(coordinates: list[Coordinates]):
    distance_matrix = []
    for i in range(len(coordinates)):
        row = []
        for j in range(len(coordinates)):
            if i == j:
                row.append(0)
            else:
                row.append(haversine(coordinates[i], coordinates[j]))
        distance_matrix.append(row)

    return distance_matrix

def calculate_route_distance(
    route: list[int],
    distance_matrix: list[list[float]],
) -> float:
    total = 0.0

    for i in range(len(route) - 1):
        start = route[i]
        end = route[i + 1]
        total += distance_matrix[start][end]
    return total

# if __name__ == "__main__":
#     lagos = Coordinates(6.5244, 3.3792)
#     london = Coordinates(51.5074, -0.1278)
#     new_york = Coordinates(40.7128, -74.0060)

#     matrix_input = [lagos, london, new_york]
    
#     matrix = build_distance_matrix(matrix_input)

#     for row in matrix:
#         print([f"{distance:.2f} km" for distance in row])