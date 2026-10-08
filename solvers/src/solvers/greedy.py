def nearest_neighbour(distance_matrix: list[list[float]],start: int = 0) -> list[int]:
    route = [start]
    visited = set(route)
    current = start

    while len(visited) < len(distance_matrix):
        nearest_index = 0
        nearest_distance = float("inf")
        for j in range(len(distance_matrix)):
            if j in visited:
                continue
            else:
                distance = distance_matrix[current][j]
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_index = j
        route.append(nearest_index)
        current = nearest_index
        visited.add(nearest_index)
    return route


# if __name__ == "__main__":
#  matrix = [
#     [0.0, 10.0, 15.0, 6.0],
#     [10.0, 0.0, 8.0, 12.0],
#     [15.0, 8.0, 0.0, 9.0],
#     [6.0, 12.0, 9.0, 0.0],
# ]

# print(nearest_neighbour(matrix, 2))