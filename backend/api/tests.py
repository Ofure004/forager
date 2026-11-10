from django.http import response
from rest_framework import status
from rest_framework.test import APITestCase

class RouteAPITests(APITestCase):
    def test_create_route(self):
        payload = {
            "locations": [
                {
                    "latitude": 6.5244,
                    "longitude": 3.3792,
                },
                {
                    "latitude": 6.6018,
                    "longitude": 3.3515,
                },
                {
                    "latitude": 6.4281,
                    "longitude": 3.4219,
                },
            ],
              "start": 0,
              "algorithm": "aco",
        }
        response = self.client.post("/api/routes/",payload,format="json",)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "route" in data
        assert len(data["route"]) == len(payload["locations"])
        assert data["route"][0] == payload["start"]
        assert "total_distance_km" in data
        assert data["total_distance_km"] > 0
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["route"][0], 0)
        self.assertEqual(len(data["route"]), 3)
        self.assertEqual(set(data["route"]), {0, 1, 2})
        self.assertGreater(data["total_distance_km"], 0)
        self.assertGreater(data["duration_minutes"], 0)
        self.assertGreater(len(data["geometry"]), 0)
