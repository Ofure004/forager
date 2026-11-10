import httpx

from solvers.distance import Coordinates


def osrm_distance_matrix(
    locations: list[Coordinates],
    base_url: str = "http://localhost:5001",
) -> list[list[float]]:
    """Return a road-distance matrix in kilometres using OSRM."""
    if not locations:
        raise ValueError("At least one location is required.")

    coordinates = ";".join(
        f"{location.longitude},{location.latitude}"
        for location in locations
    )

    url = f"{base_url.rstrip('/')}/table/v1/driving/{coordinates}"

    response = httpx.get(
        url,
        params={"annotations": "distance"},
        timeout=30.0,
    )
    response.raise_for_status()

    data = response.json()

    if data.get("code") != "Ok":
        raise RuntimeError(
            f"OSRM table request failed: {data.get('code')}"
        )

    distances = data.get("distances")
    if any(
        distance is None
        for row in distances
        for distance in row
    ):
        raise ValueError(
            "OSRM returned unreachable location pairs. "
            "Check the coordinates and road network coverage."
        )

    return [
        [distance / 1000 for distance in row]
        for row in distances
    ]