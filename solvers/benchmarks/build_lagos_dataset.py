import json
import time
from pathlib import Path
import httpx


DATASET_PATH = Path(__file__).parents[1] / "data" / "lagos_locations.json"

# These are recognizable landmarks and neighbourhood hubs used as
# proxies for delivery destinations, not actual customer addresses.
LOCATIONS = [
    "Computer Village, Ikeja",
    "Allen Avenue, Ikeja",
    "Opebi, Ikeja",
    "Ogba, Ikeja, Lagos",
    "Ojodu Berger, Lagos",
    "Agege Stadium, Agege, Lagos",
    "Abule Egba, Lagos",
    "Dopemu, Lagos",
    "Iyana Ipaja, Lagos",
    "Egbeda, Lagos",
    "Ikotun, Lagos",
    "Oshodi Transport Interchange, Lagos",
    "Mafoluku, Lagos",
    "Ladipo Market, Mushin",
    "Mushin, Lagos",
    "Idi Oro, Mushin",
    "Jibowu, Lagos",
    # "Stadium Hotel, Surulere, Lagos",
    "Yaba College of Technology, Yaba, Lagos",
    "University of Lagos, Akoka, Lagos",
    "Onipanu, Lagos",
    "Fadeyi, Lagos",
    "Palmgrove, Lagos",
    "Anthony Village, Lagos",
    "Maryland, Lagos",
    "Gbagada, Lagos",
    "Ifako, Gbagada",
    "Bariga, Lagos",
    "Somolu, Lagos",
    "Ilupeju, Lagos",
    "Town Planning Way, Ilupeju",
    "National Stadium, Surulere",
    "Teslim Balogun Stadium, Surulere",
    "Ojuelegba, Lagos",
    "Lawanson, Surulere",
    "Ijesha, Surulere",
    "Coker, Surulere",
    "Orile, Lagos",
    "Costain, Lagos",
    "Ebute Metta, Lagos",
    "Oyingbo Bus Terminal, Lagos",
    "Iddo, Lagos",
    "Apapa, Lagos",
    "Ajegunle, Lagos",
    "Amukoko, Lagos",
    "Iganmu, Lagos",
    "Ketu, Lagos",
    "Mile 12, Lagos",
    "Ojota, Lagos",
    "Magodo, Lagos",
]


def geocode_location(
    client: httpx.Client,
    location: str,
) -> dict | None:
    response = client.get(
        "https://nominatim.openstreetmap.org/search",
        params={
            "q": f"{location}, Lagos, Nigeria",
            "format": "jsonv2",
            "limit": 1,
            "countrycodes": "ng",
        },
    )
    response.raise_for_status()

    results = response.json()

    if not results:
        return None

    result = results[0]

    return {
        "id": "",
        "name": location,
        "latitude": float(result["lat"]),
        "longitude": float(result["lon"]),
        "resolved_as": result["display_name"],
    }

def main():
    with DATASET_PATH.open(encoding="utf-8") as file:
        dataset = json.load(file)

    # Retain only entries that still belong to the current location list.
    valid_names = set(LOCATIONS)

    deliveries = [
        delivery
        for delivery in dataset.get("deliveries", [])
        if delivery["name"] in valid_names
    ]

    unresolved = []

    # Avoid repeating successful geocoding requests on subsequent runs.
    resolved_names = {delivery["name"] for delivery in deliveries}

    headers = {
        "User-Agent": "ForagerRouteBenchmark/1.0 (local research project)"
    }

    with httpx.Client(
        headers=headers,
        timeout=20.0,
    ) as client:
        for index, location in enumerate(LOCATIONS, start=1):

            if location in resolved_names:
                print(f"[{index}/{len(LOCATIONS)}] Already resolved: {location}")
                continue

            print(f"[{index}/{len(LOCATIONS)}] Resolving {location}...")

            delivery = geocode_location(client, location)

            if delivery is None:
                print(f"    !! Could not resolve: {location}")
                unresolved.append(location)
            else:
                delivery["id"] = f"delivery-{index:03d}"
                deliveries.append(delivery)
                resolved_names.add(location)

                print(f"    -> {delivery['resolved_as']}")

            # Persist progress after every lookup.
            dataset["deliveries"] = deliveries
            dataset["unresolved_locations"] = unresolved

            with DATASET_PATH.open("w", encoding="utf-8") as file:
                json.dump(dataset, file, indent=2, ensure_ascii=False)

            time.sleep(1.1)

    print("\nDataset generation complete.")
    print(f"Resolved: {len(deliveries)}/50")
    print(f"Unresolved: {len(unresolved)}")

    if unresolved:
        print("\nLocations requiring attention:")
        for location in unresolved:
            print(f" - {location}")


if __name__ == "__main__":
    main()
