# Forager: Comparative Analysis Tool for Deliveries

This project figures out the best way to deliver a pile of orders with a limited number of riders — who carries what, and in what order — so the whole run takes as little driving as possible.

It's the kind of problem every delivery business faces: ten riders, eighty orders, everyone has a limited bag size and a shift that ends at a certain time, and some orders need to arrive within a specific window. Deciding who goes where, in what sequence, gets hard fast. This tool does that deciding.

## The interesting part

There are lots of ways to solve vehicle routing problems. This project includes three and lets you compare them side by side:

- **Nearest-neighbour (greedy)** — always send each rider to their nearest unvisited stop. Quick to compute, but not very smart.
- **Ant Colony Optimisation** — the one built by hand. It mimics how a colony of ants finds short paths to food: lots of them wander, they leave pheromone trails on good routes, and over time the colony converges on something efficient.
- **Google OR-Tools** — Google's operations-research routing solver, used as the yardstick to measure the other two against.

Running all three on the same set of orders shows the trade-offs clearly: which is fastest to compute, which finds the shortest routes, and where each one starts to struggle.

## What you can do with it

- Load a set of orders and riders and generate a delivery plan
- Watch the routes draw themselves on a map
- Watch the ant colony approach "think" — trails it favours get stronger as it settles on an answer
- Compare all three approaches on the same orders and see the numbers
- Drop a new order in while riders are already out and have the plan adjust on the fly

## Project structure

```
backend/    Django API — stores orders and riders, runs the solvers
frontend/   Next.js app — the map and the UI you actually interact with
solvers/    The three routing algorithms, kept as a standalone package
infra/      Setup for the OSRM mapping engine and local environment
```

The routing logic in `solvers/` is deliberately kept separate from everything else. It doesn't know or care that there's a website or a database attached — you hand it a list of stops and it hands back routes. That separation makes it easy to test routing on its own and swap approaches in and out.

## Tech stack

| Layer     | Technology                        |
| --------- | --------------------------------- |
| Backend   | Python 3.12+, Django, DRF         |
| Frontend  | Next.js, React, Tailwind CSS      |
| Database  | PostgreSQL (SQLite for dev)        |
| Distances | Self-hosted OSRM on real map data  |

OSRM runs locally on real OpenStreetMap data so the project gets actual driving distances without racking up fees on a paid maps API.

## Getting started

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [Bun](https://bun.sh/) (JS runtime / package manager)
- Docker (for OSRM)

### Backend

```bash
cd backend
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

### Frontend

```bash
cd frontend/frontend
bun install
bun dev
```

### OSRM (distance engine)

See [`infra/`](infra/) for setup instructions.

## License

This project is not currently licensed for redistribution.
