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
  const [greedyRoute, setGreedyRoute] = useState<RouteResponse | null>(null);
  const [acoRoute, setAcoRoute] = useState<RouteResponse | null>(null);
  const [routeError, setRouteError] = useState<string | null>(null);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState("Greedy");

  useEffect(() => {
    let cancelled = false;

    const handleRouteError = () => {
      if (!cancelled) {
        setRouteError("Could not load route results. Check that the API and OSRM are running.");
      }
    };

    createRoute(locations, 0, "greedy").then((route) => {
      if (!cancelled) setGreedyRoute(route);
    }).catch(handleRouteError);

    createRoute(locations, 0, "aco").then((route) => {
      if (!cancelled) setAcoRoute(route);
    }).catch(handleRouteError);

    return () => {
      cancelled = true;
    };
  }, []);

  const comparisons = [
    ...(greedyRoute
      ? [
          {
            algorithm: "Greedy",
            distance: greedyRoute.total_distance_km,
            duration: greedyRoute.duration_minutes,
            optimizationTime: greedyRoute.optimization_time_ms,
            route: greedyRoute.route,
          },
        ]
      : []),
    ...(acoRoute
      ? [
          {
            algorithm: "ACO",
            distance: acoRoute.total_distance_km,
            duration: acoRoute.duration_minutes,
            optimizationTime: acoRoute.optimization_time_ms,
            route: acoRoute.route,
          },
        ]
      : []),
  ];
  const selectedRoute = selectedAlgorithm === "ACO" ? acoRoute : greedyRoute;

  return (
    <main className="relative h-dvh w-full overflow-hidden">
      <Map center={[3.4219, 6.4281]} zoom={11} className="absolute inset-0">
        <MapControls position="top-right" showZoom showCompass />

        <MapRoute coordinates={selectedRoute?.geometry ?? []} />

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

      {comparisons.length > 0 && (
        <RouteComparison
          results={comparisons}
          locations={locations}
          selectedAlgorithm={selectedAlgorithm}
          onSelectAlgorithm={setSelectedAlgorithm}
          greedyReady={greedyRoute !== null}
          acoReady={acoRoute !== null}
        />
      )}
      {routeError && (
        <div className="absolute left-4 top-4 z-20 max-w-sm rounded-xl border border-red-200 bg-white/95 px-4 py-3 text-sm text-red-700 shadow-xl sm:left-6 sm:top-6">
          {routeError}
        </div>
      )}
    </main>
  );
}
