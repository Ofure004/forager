"use client";

import { Route as RouteIcon, Sparkles } from "lucide-react";

type Location = {
  name: string;
  address?: string;
  type?: "start" | "delivery";
};

export type AlgorithmResult = {
  algorithm: string;
  distance: number;
  duration: number;
  /** Location indexes in the order visited, including the starting depot. */
  route?: number[];
  optimizationTime: number;
};

type RouteComparisonProps = {
  results: AlgorithmResult[];
  locations: Location[];
  selectedAlgorithm: string;
  onSelectAlgorithm: (algorithm: string) => void;
  greedyReady: boolean;
  acoReady: boolean;
};

export function RouteComparison({
  results,
  locations,
  selectedAlgorithm,
  onSelectAlgorithm,
  greedyReady,
  acoReady,
}: RouteComparisonProps) {
  const selected = results.find(
    (result) => result.algorithm === selectedAlgorithm,
  );
  return (
    <section className="absolute left-4 top-4 z-20 flex max-h-[calc(100dvh-2rem)] w-[min(390px,calc(100%-2rem))] flex-col overflow-hidden rounded-2xl border border-white/70 bg-white/95 shadow-2xl shadow-slate-950/20 backdrop-blur-xl sm:left-6 sm:top-6 sm:max-h-[calc(100dvh-3rem)]">
      <header className="shrink-0 px-5 pb-4 pt-5">
        <div className="mb-4 flex items-start justify-between gap-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
              Route comparison
            </p>
            <p className="mt-1 text-sm text-slate-600">
              Compare distance, travel time, compute time, and stop order
            </p>
          </div>
          <span className="inline-flex shrink-0 items-center gap-1 rounded-full bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700 ring-1 ring-inset ring-blue-600/15">
            <Sparkles className="size-3" /> {results.length} algorithms
          </span>
        </div>

        <div
          className="grid grid-cols-2 gap-1 rounded-xl bg-slate-100 p-1"
          role="group"
          aria-label="Choose route algorithm"
        >
          {["Greedy", "ACO"].map((algorithm) => {
            const active = algorithm === selectedAlgorithm;
            const disabled =
              (algorithm === "Greedy" && !greedyReady) ||
              (algorithm === "ACO" && !acoReady);
            return (
              <button
                key={algorithm}
                type="button"
                aria-pressed={active}
                disabled={disabled}
                onClick={() => onSelectAlgorithm(algorithm)}
                className={`rounded-lg px-3 py-2 text-sm font-semibold transition-colors disabled:cursor-not-allowed disabled:opacity-45 ${active ? "bg-white text-blue-700 shadow-sm" : "text-slate-500 hover:text-slate-800"}`}
              >
                {algorithm}
              </button>
            );
          })}
        </div>
        {selected && (
          <div
            className="mt-3 grid grid-cols-3 divide-x divide-slate-200 rounded-xl bg-slate-50 px-3 py-3"
            aria-live="polite"
          >
            <div className="pr-3">
              <p className="text-xs font-medium text-slate-500">Distance</p>
              <p className="mt-1 text-xl font-bold tracking-tight text-slate-950">
                {selected.distance.toFixed(2)}{" "}
                <span className="text-sm font-semibold">km</span>
              </p>
            </div>
            <div className="px-3">
              <p className="text-xs font-medium text-slate-500">
                Estimated time
              </p>
              <p className="mt-1 text-xl font-bold tracking-tight text-slate-950">
                {selected.duration.toFixed(1)}{" "}
                <span className="text-sm font-semibold">min</span>
              </p>
            </div>
            <div className="pl-3">
              <p className="text-xs font-medium text-slate-500">Compute time</p>
              <p className="mt-1 text-xl font-bold tracking-tight text-slate-950">
                {selected.optimizationTime.toFixed(2)}{" "}
                <span className="text-sm font-semibold">ms</span>
              </p>
            </div>
          </div>
        )}
      </header>

      <div className="min-h-0 overflow-y-auto border-t border-slate-200/80 px-5 py-4">
        <div className="mb-3 flex items-center justify-between">
          <div>
            <p className="text-sm font-semibold text-slate-900">
              {selected?.algorithm ?? "Route"} decisions
            </p>
            <p className="text-xs text-slate-500">
              Visit order chosen by this algorithm
            </p>
          </div>
          <RouteIcon className="size-4 text-slate-400" />
        </div>
        {selected?.route?.length ? (
          <div className="max-h-36 space-y-1 overflow-y-auto">
            {selected.route.map((locationIndex, index) => {
              const location = locations[locationIndex];
              if (!location) return null;
              return (
                <div
                  key={`${locationIndex}-${index}`}
                  className="flex items-center gap-3 rounded-lg px-2 py-1.5"
                >
                  <span
                    className={`flex size-6 shrink-0 items-center justify-center rounded-full text-[10px] font-bold ${index === 0 ? "bg-blue-600 text-white" : "border border-slate-200 bg-white text-slate-600"}`}
                  >
                    {index === 0 ? "S" : index}
                  </span>
                  <span className="min-w-0 flex-1 truncate text-sm font-medium text-slate-800">
                    {location.name}
                  </span>
                  {index === 0 && (
                    <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                      Start
                    </span>
                  )}
                </div>
              );
            })}
          </div>
        ) : (
          <p className="rounded-lg bg-slate-50 px-3 py-2.5 text-xs leading-relaxed text-slate-500">
            Stop order will appear when this algorithm returns its route
            sequence.
          </p>
        )}
      </div>
    </section>
  );
}
