from dataclasses import dataclass
import requests
from solvers.distance import Coordinates


@dataclass
class Route:
    distance_km: float
    duration_minutes: float
    geometry: list[list[float]]


class OSRMClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def route(self, coordinates: list[Coordinates]) -> Route:
        coordinate_string = ";".join(
            f"{coordinate.longitude},{coordinate.latitude}"
            for coordinate in coordinates
        )

        url = f"{self.base_url}/route/v1/driving/{coordinate_string}"

        response = requests.get(
            url,
            params={
                "overview": "full",
                "geometries": "geojson",
            },
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        route = data["routes"][0]

        return Route(
            distance_km=route["distance"] / 1000,
            duration_minutes=route["duration"] / 60,
            geometry=route["geometry"]["coordinates"],
        )