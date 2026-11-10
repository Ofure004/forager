import json
import random
import statistics
import time
from pathlib import Path

from solvers.aco import ant_colony
from solvers.greedy import nearest_neighbour
from solvers.ortools_solver import ortools_route

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
MATRIX_PATH = DATA_DIR / "lagos_distance_matrix.json"


def load_distance_matrix():
    with MATRIX_PATH.open(encoding="utf-8") as file:
        data = json.load(file)

    locations = data["locations"]
    matrix = data["matrix"]

    expected_size = len(locations)

    if len(matrix) != expected_size:
        raise ValueError("Distance matrix row count does not match locations.")

    if any(len(row) != expected_size for row in matrix):
        raise ValueError("Distance matrix is not square.")

    if expected_size != 51:
        raise ValueError(
            f"Expected 51 locations (1 depot + 50 deliveries), "
            f"got {expected_size}."
        )

    return locations, matrix


def select_problem_instance(
    locations,
    full_matrix,
    n: int,
    seed: int,
):
    """Select the depot and n deliveries, then extract their distance matrix."""

    delivery_indices = list(range(1, len(locations)))

    if n > len(delivery_indices):
        raise ValueError(f"Cannot select {n} deliveries.")

    rng = random.Random(seed)
    selected_indices = sorted(rng.sample(delivery_indices, n))

    # Index 0 is always the depot.
    indices = [0, *selected_indices]

    submatrix = [
        [full_matrix[i][j] for j in indices]
        for i in indices
    ]

    selected_locations = [locations[i] for i in indices]

    return selected_locations, submatrix
def route_distance(
    route: list[int],
    distance_matrix: list[list[float]],
) -> float:
    return sum(
        distance_matrix[route[i]][route[i + 1]]
        for i in range(len(route) - 1)
    )


def benchmark_algorithm(
    name,
    solver,
    distance_matrix,
    runs=10,
    time_limit_ms: int = 1000,
):
    elapsed_times = []
    route_distances = []
    routes = []

    for run in range(runs):
        start_time = time.perf_counter()

        if name == "ACO":
            route = solver(
                distance_matrix,
                start=0,
                seed=run,
            )
        elif name == "OR-Tools":
            route = solver(distance_matrix, start=0, time_limit_ms=time_limit_ms)
        else:
            route = solver(distance_matrix, start=0)
        routes.append(tuple(route))

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        elapsed_times.append(elapsed_ms)
        route_distances.append(
            route_distance(route, distance_matrix)
        )

    return {
        "algorithm": name,
        "runs": runs,
        "average_time_ms": statistics.mean(elapsed_times),
        "median_time_ms": statistics.median(elapsed_times),
        "best_distance": min(route_distances),
        "average_distance": statistics.mean(route_distances),
        "worst_distance": max(route_distances),
        "distance_std_dev": statistics.pstdev(route_distances),
        "unique_routes": len(set(routes)),
    }


if __name__ == "__main__":
    problem_sizes = [4, 10, 25, 50]
    instances_per_size = 5
    tie_tolerance = 0.01

    locations, full_matrix = load_distance_matrix()

    print(f"Loaded {len(locations)} locations from saved OSRM matrix.")
    print(f"Depot: {locations[0]['name']}")

    for n in problem_sizes:
        print(f"\n{'=' * 65}")
        print(f"BENCHMARK: {n} LOCATIONS")
        print("=" * 65)

        # Keep results separate for each algorithm.
        aco_improvements = []
        ortools_improvements = []

        instance_greedy_distances = []
        instance_aco_distances = []
        instance_ortools_distances = []

        instance_greedy_times = []
        instance_aco_times = []
        instance_ortools_times = []
        time_limit_ms = 250

        aco_wins = aco_losses = aco_ties = 0
        ortools_wins = ortools_losses = ortools_ties = 0

        # The complete dataset contains exactly 50 deliveries.
        # Smaller problems use five different deterministic subsets.
        instance_count = 1 if n == 50 else instances_per_size

        if n == 50:
            print("Using the complete 50-delivery dataset.")

        for instance in range(instance_count):
            selected_locations, distance_matrix = select_problem_instance(
                locations,
                full_matrix,
                n=n,
                seed=1000 + n * 100 + instance,
            )

            greedy = benchmark_algorithm(
                "Greedy",
                nearest_neighbour,
                distance_matrix,
                runs=10,
            )

            aco = benchmark_algorithm(
                "ACO",
                ant_colony,
                distance_matrix,
                runs=30,
            )

            ortools = benchmark_algorithm(
                "OR-Tools",
                ortools_route,
                distance_matrix,
                runs=5,
                time_limit_ms=250,
            )

            greedy_distance = greedy["average_distance"]
            aco_distance = aco["average_distance"]
            ortools_distance = ortools["average_distance"]

            # Positive improvement means a shorter route than Greedy.
            aco_improvement = (
                (greedy_distance - aco_distance)
                / greedy_distance
                * 100
            )

            ortools_improvement = (
                (greedy_distance - ortools_distance)
                / greedy_distance
                * 100
            )

            aco_improvements.append(aco_improvement)
            ortools_improvements.append(ortools_improvement)

            instance_greedy_distances.append(greedy_distance)
            instance_aco_distances.append(aco_distance)
            instance_ortools_distances.append(ortools_distance)

            instance_greedy_times.append(greedy["average_time_ms"])
            instance_aco_times.append(aco["average_time_ms"])
            instance_ortools_times.append(ortools["average_time_ms"])

            # Count wins, losses and ties separately against Greedy.
            if aco_improvement > tie_tolerance:
                aco_wins += 1
            elif aco_improvement < -tie_tolerance:
                aco_losses += 1
            else:
                aco_ties += 1

            if ortools_improvement > tie_tolerance:
                ortools_wins += 1
            elif ortools_improvement < -tie_tolerance:
                ortools_losses += 1
            else:
                ortools_ties += 1

            print(
                f"Instance {instance + 1}: "
                f"Greedy={greedy_distance:.2f} km, "
                f"ACO={aco_distance:.2f} km, "
                f"OR-Tools={ortools_distance:.2f} km, "
                f"ACO improvement={aco_improvement:+.2f}%, "
                f"OR-Tools improvement={ortools_improvement:+.2f}%, "
                f"  OR-Tools budget={time_limit_ms} ms, "
                f"measured={ortools['average_time_ms']:.2f} ms"
            )
            print(
                f"  OR-Tools across {ortools['runs']} runs: "
                f"best={ortools['best_distance']:.2f} km, "
                f"mean={ortools['average_distance']:.2f} km, "
                f"worst={ortools['worst_distance']:.2f} km, "
                f"std dev={ortools['distance_std_dev']:.3f} km, "
                f"unique routes={ortools['unique_routes']}, "
            )
        print("\nSUMMARY ACROSS INSTANCES")

        print(
            f"ACO mean improvement: "
            f"{statistics.mean(aco_improvements):+.2f}%"
        )
        print(
            f"ACO median improvement: "
            f"{statistics.median(aco_improvements):+.2f}%"
        )
        print(
            f"ACO vs Greedy: {aco_wins} wins, "
            f"{aco_losses} losses, {aco_ties} ties "
            f"(out of {instance_count})"
        )

        print(
            f"OR-Tools mean improvement: "
            f"{statistics.mean(ortools_improvements):+.2f}%"
        )
        print(
            f"OR-Tools median improvement: "
            f"{statistics.median(ortools_improvements):+.2f}%"
        )
        print(
            f"OR-Tools vs Greedy: {ortools_wins} wins, "
            f"{ortools_losses} losses, {ortools_ties} ties "
            f"(out of {instance_count})"
        )

        print(
            f"Mean Greedy distance: "
            f"{statistics.mean(instance_greedy_distances):.2f} km"
        )
        print(
            f"Mean ACO distance: "
            f"{statistics.mean(instance_aco_distances):.2f} km"
        )
        print(
            f"Mean OR-Tools distance: "
            f"{statistics.mean(instance_ortools_distances):.2f} km"
        )

        print(
            f"Mean Greedy runtime: "
            f"{statistics.mean(instance_greedy_times):.2f} ms"
        )
        print(
            f"Mean ACO runtime: "
            f"{statistics.mean(instance_aco_times):.2f} ms"
        )
        print(
            f"Mean OR-Tools runtime: "
            f"{statistics.mean(instance_ortools_times):.2f} ms"
        )
