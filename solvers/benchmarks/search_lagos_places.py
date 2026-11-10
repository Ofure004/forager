import httpx

headers = {
    "User-Agent": "ForagerRouteBenchmark/1.0 (local research project)"
}

params = {
    "q": "Iganmu, Surulere, Lagos, Nigeria",
    "format": "jsonv2",
    "limit": 10,
    "countrycodes": "ng",
    "addressdetails": 1,
}

response = httpx.get(
    "https://nominatim.openstreetmap.org/search",
    params=params,
    headers=headers,
    timeout=20.0,
)
response.raise_for_status()

for result in response.json():
    print(f"\nName: {result['display_name']}")
    print(f"Latitude: {result['lat']}")
    print(f"Longitude: {result['lon']}")
    print(f"Type: {result.get('type')}")
