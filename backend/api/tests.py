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
        }
        response = self.client.post("/api/routes/",payload,format="json",)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "route" in data
        assert len(data["route"]) == len(payload["locations"])
        assert data["route"][0] == payload["start"]
        assert "total_distance_km" in data
        assert data["total_distance_km"] > 0
