import random


def ant_colony(
    distance_matrix: list[list[float]],
    start: int = 0,
    n_ants: int = 20,
    n_iterations: int = 100,
    alpha: float = 1.0,
    beta: float = 2.0,
    evaporation_rate: float = 0.5,
    seed: int | None = None,
) -> list[int]:

    if seed is not None:
        random.seed(seed)
    n = len(distance_matrix)

    pheromone = [
        [1.0 for _ in range(n)]
        for _ in range(n)
    ]

    best_route: list[int] = []
    best_distance = float("inf")

    for _ in range(n_iterations):
        routes = []

        for _ in range(n_ants):
            route = [start]
            unvisited = set(range(n)) - {start}

            while unvisited:
                current = route[-1]

                probabilities = []
                total_probability = 0.0

                for candidate in unvisited:
                    distance = distance_matrix[current][candidate]

                    if distance == 0:
                        probability = 0.0
                    else:
                        probability = (
                            pheromone[current][candidate] ** alpha
                            * (1 / distance) ** beta
                        )

                    probabilities.append((candidate, probability))
                    total_probability += probability

                if total_probability == 0:
                    next_node = random.choice(list(unvisited))
                else:
                    threshold = random.random() * total_probability
                    cumulative = 0.0
                    next_node = next(
                        candidate
                        for candidate, probability in probabilities
                        if (cumulative := cumulative + probability) >= threshold
                    )

                route.append(next_node)
                unvisited.remove(next_node)

            routes.append(route)

        for route in routes:
            distance = sum(
                distance_matrix[route[i]][route[i + 1]]
                for i in range(len(route) - 1)
            )

            if distance < best_distance:
                best_distance = distance
                best_route = route

        for i in range(n):
            for j in range(n):
                pheromone[i][j] *= 1 - evaporation_rate

        for route in routes:
            distance = sum(
                distance_matrix[route[i]][route[i + 1]]
                for i in range(len(route) - 1)
            )

            if distance == 0:
                continue

            deposit = 1 / distance

            for i in range(len(route) - 1):
                current = route[i]
                next_node = route[i + 1]
                pheromone[current][next_node] += deposit

    return best_route
