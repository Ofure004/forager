"use client";

import {
  Map,
  MapControls,
  MapMarker,
  MarkerContent,
  MarkerLabel,
  MarkerPopup,
  MapRoute,
} from "@/components/ui/map";
import { createRoute, RouteResponse } from "@/lib/routes";
import { useEffect, useState } from "react";
import { RouteComparison } from "@/components/route-comparison";

type Location = {
  id: number;
  name: string;
  address: string;
  longitude: number;
  latitude: number;
  type: "start" | "delivery";
};

const locations: Location[] = [
  {
    id: 0,
    name: "Warehouse",
    address: "Victoria Island",
    longitude: 3.4219,
    latitude: 6.4281,
    type: "start",
  },
  {
    id: 1,
    name: "Customer A",
    address: "Lekki Phase 1",
    longitude: 3.4698,
    latitude: 6.4474,
    type: "delivery",
  },
  {
    id: 2,
    name: "Customer B",
    address: "Yaba",
    longitude: 3.3841,
    latitude: 6.5158,
    type: "delivery",
  },
];

export default function Home() {
  const [route, setRoute] = useState<RouteResponse | null>(null);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState("Greedy");

  const comparisons = route
    ? [
        {
          algorithm: "Greedy",
          distance: route.total_distance_km,
          duration: route.duration_minutes,
          route: route.route,
        },
        { algorithm: "ACO", distance: 24.91, duration: 26.8, example: true },
        { algorithm: "OR-Tools", distance: 24.72, duration: 26.4, example: true },
      ]
    : [];

  useEffect(() => {
    createRoute(locations).then((result) => {
      setRoute(result);
    });
  }, []);
  return (
    <main className="relative h-dvh w-full overflow-hidden">
      <Map center={[3.4219, 6.4281]} zoom={11} className="absolute inset-0">
        <MapControls position="top-right" showZoom showCompass />

        <MapRoute coordinates={route?.geometry ?? []} />

        {locations.map((location) => (
          <MapMarker
            key={location.id}
            longitude={location.longitude}
            latitude={location.latitude}
          >
            <MarkerContent>
              <div
                className={
                  location.type === "start"
                    ? "h-5 w-5 rounded-full border-2 border-white bg-primary shadow-lg"
                    : "h-4 w-4 rounded-full border-2 border-white bg-primary shadow-lg"
                }
              />
            </MarkerContent>

            <MarkerLabel>{location.name}</MarkerLabel>

            <MarkerPopup>
              <div className="space-y-1">
                <p className="font-medium">{location.name}</p>
                <p className="text-sm text-muted-foreground">
                  {location.address}
                </p>
              </div>
            </MarkerPopup>
          </MapMarker>
        ))}
      </Map>

      {route && (
        <RouteComparison
          results={comparisons}
          locations={locations}
          selectedAlgorithm={selectedAlgorithm}
          onSelectAlgorithm={setSelectedAlgorithm}
        />
      )}
    </main>
  );
}
