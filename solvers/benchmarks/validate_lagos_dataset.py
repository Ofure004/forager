
import json
import math
from itertools import combinations
from pathlib import Path

DATASET_PATH = Path(__file__).parents[1] / "data" / "lagos_locations.json"

# Flag points within this distance for manual review.
PROXIMITY_THRESHOLD_METRES = 250


def haversine(a: dict, b: dict) -> float:
    """Calculate straight-line distance between two coordinates in metres."""
    earth_radius = 6_371_000

    lat1 = math.radians(a["latitude"])
    lon1 = math.radians(a["longitude"])
    lat2 = math.radians(b["latitude"])
    lon2 = math.radians(b["longitude"])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    h = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    return 2 * earth_radius * math.asin(math.sqrt(h))


def validate_coordinates(location: dict) -> list[str]:
    errors = []

    latitude = location.get("latitude")
    longitude = location.get("longitude")

    if not isinstance(latitude, (int, float)) or not math.isfinite(latitude):
        errors.append("Invalid latitude")
    elif not -90 <= latitude <= 90:
        errors.append("Latitude outside valid range")

    if not isinstance(longitude, (int, float)) or not math.isfinite(longitude):
        errors.append("Invalid longitude")
    elif not -180 <= longitude <= 180:
        errors.append("Longitude outside valid range")

    return errors


def main():
    with DATASET_PATH.open(encoding="utf-8") as file:
        dataset = json.load(file)

    depot = dataset["depot"]
    deliveries = dataset["deliveries"]

    print("=== STRUCTURAL VALIDATION ===")

    print(f"Delivery count: {len(deliveries)}")
    print(f"Unique IDs: {len({x['id'] for x in deliveries})}")
    print(f"Unique names: {len({x['name'] for x in deliveries})}")

    errors = []

    if len(deliveries) != 50:
        errors.append(f"Expected 50 deliveries, found {len(deliveries)}")

    ids = [x["id"] for x in deliveries]
    names = [x["name"] for x in deliveries]

    if len(ids) != len(set(ids)):
        errors.append("Duplicate delivery IDs")

    if len(names) != len(set(names)):
        errors.append("Duplicate delivery names")

    all_locations = [depot, *deliveries]

    for location in all_locations:
        for error in validate_coordinates(location):
            errors.append(f"{location.get('name', location.get('id'))}: {error}")

    print(f"Depot: {depot['name']}")
    print(f"Total locations including depot: {len(all_locations)}")

    print("\n=== GEOGRAPHIC VALIDATION ===")

    # Find pairs of delivery points that are suspiciously close.
    close_pairs = []

    for a, b in combinations(deliveries, 2):
        distance = haversine(a, b)

        if distance < PROXIMITY_THRESHOLD_METRES:
            close_pairs.append((distance, a, b))

    close_pairs.sort(key=lambda item: item[0])

    print(f"Pairs closer than {PROXIMITY_THRESHOLD_METRES}m: {len(close_pairs)}")

    for distance, a, b in close_pairs:
        print(
            f"  {distance:.1f}m | "
            f"{a['name']} <-> {b['name']}"
        )

    # Show the geographic bounding box.
    latitudes = [x["latitude"] for x in all_locations]
    longitudes = [x["longitude"] for x in all_locations]

    print("\nGeographic bounds:")
    print(f"  Latitude:  {min(latitudes):.5f} to {max(latitudes):.5f}")
    print(f"  Longitude: {min(longitudes):.5f} to {max(longitudes):.5f}")

    print("\n=== RESULT ===")

    if errors:
        print("VALIDATION ERRORS:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("No structural or coordinate-range errors found.")

    if close_pairs:
        print("Review the close pairs before using this dataset.")
    else:
        print("No delivery points fall within the proximity threshold.")


if __name__ == "__main__":
    main()
