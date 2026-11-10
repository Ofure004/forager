
import json
import math
from pathlib import Path

from solvers.distance import Coordinates
from solvers.osrm import osrm_distance_matrix


DATASET_PATH = Path(__file__).parents[1] / "data" / "lagos_locations.json"


def main():
    with DATASET_PATH.open(encoding="utf-8") as file:
        dataset = json.load(file)

    locations = [dataset["depot"], *dataset["deliveries"]]

    coordinates = [
        Coordinates(
            latitude=location["latitude"],
            longitude=location["longitude"],
        )
        for location in locations
    ]

    print(f"Requesting OSRM matrix for {len(coordinates)} locations...")

    matrix = osrm_distance_matrix(coordinates)

    expected_size = len(locations)

    # Check matrix dimensions.
    if len(matrix) != expected_size:
        raise ValueError(
            f"Expected {expected_size} rows, got {len(matrix)}."
        )

    for index, row in enumerate(matrix):
        if len(row) != expected_size:
            raise ValueError(
                f"Row {index} has {len(row)} values; "
                f"expected {expected_size}."
            )

    # Find invalid or unreachable distances.
    invalid_pairs = []

    for i, row in enumerate(matrix):
        for j, distance in enumerate(row):
            if not math.isfinite(distance) or distance < 0:
                invalid_pairs.append((i, j, distance))

    if invalid_pairs:
        print(f"\nFound {len(invalid_pairs)} invalid/unreachable pairs:")

        for i, j, distance in invalid_pairs[:20]:
            print(
                f"  {locations[i]['name']} -> "
                f"{locations[j]['name']}: {distance}"
            )

        raise ValueError("OSRM matrix contains invalid distances.")

    # Check diagonal values.
    diagonal_errors = [
        i for i in range(expected_size)
        if not math.isclose(matrix[i][i], 0.0, abs_tol=0.001)
    ]

    if diagonal_errors:
        raise ValueError(
            f"Expected zero diagonal distances; "
            f"problematic indices: {diagonal_errors}"
        )

    # Summarize the matrix.
    distances = [
        matrix[i][j]
        for i in range(expected_size)
        for j in range(expected_size)
        if i != j
    ]
    matrix_path = DATASET_PATH.with_name("lagos_distance_matrix.json")

    matrix_data = {
    "metadata": {
        "source": "OSRM",
        "profile": "driving",
        "unit": "kilometres",
        "location_count": len(locations),
        # "depot_id": depot["id"],
    },
    "locations": [
        {
            "id": location.get("id", "depot-ikeja"),
            "name": location["name"],
        }
        for location in locations
    ],
    "matrix": matrix,
    }

    with matrix_path.open("w", encoding="utf-8") as file:
        json.dump(matrix_data, file, indent=2)

    print(f"Saved distance matrix to: {matrix_path}")

    print("\n=== OSRM MATRIX VALIDATION ===")
    print(f"Locations: {expected_size}")
    print(f"Matrix dimensions: {len(matrix)} x {len(matrix[0])}")
    print(f"Distance pairs checked: {len(distances)}")
    print(f"Minimum road distance: {min(distances):.2f} km")
    print(f"Maximum road distance: {max(distances):.2f} km")
    print(f"Average road distance: {sum(distances) / len(distances):.2f} km")
    print(f"Invalid distances: {len(invalid_pairs)}")
    print(f"Diagonal errors: {len(diagonal_errors)}")

    print("\nAll OSRM matrix checks passed.")


if __name__ == "__main__":
    main()
