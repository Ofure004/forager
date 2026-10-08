from infra.src.infra.osrm import OSRMClient
from solvers.distance import Coordinates


client = OSRMClient("http://localhost:5001")

coordinates = [
    Coordinates(latitude=6.4281, longitude=3.4219),
    Coordinates(latitude=6.4474, longitude=3.4698),
    Coordinates(latitude=6.5158, longitude=3.3841),
]

route = client.route(coordinates)

print(f"Distance: {route.distance_km:.2f} km")
print(f"Duration: {route.duration_minutes:.2f} minutes")
print(f"Geometry points: {len(route.geometry)}")