export type Location = {
  longitude: number;
  latitude: number;
};

export type RouteResponse = {
  route: number[];
  total_distance_km: number;
  duration_minutes: number;
  optimization_time_ms: number;
  geometry: [number, number][];
};

export async function createRoute(
  locations: Location[],
  start = 0,
  algorithm: "greedy" | "aco" = "greedy",
): Promise<RouteResponse> {
  const response = await fetch("http://localhost:8000/api/routes/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      locations,
      start,
      algorithm,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to create route");
  }

  return response.json();
}
