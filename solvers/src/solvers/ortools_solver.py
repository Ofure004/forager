from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def ortools_route(
    distance_matrix: list[list[float]],
    start: int = 0,
    time_limit_ms: int = 1000,
) -> list[int]:
    """Find an open route visiting every location exactly once."""
    n = len(distance_matrix)

    if n == 0:
        raise ValueError("distance_matrix must not be empty")

    if any(len(row) != n for row in distance_matrix):
        raise ValueError("distance_matrix must be square")

    if not 0 <= start < n:
        raise ValueError("start must be a valid location index")

    if n == 1:
        return [start]

    # OR-Tools routing costs must be integers.
    scale = 1000
    costs = [
        [round(distance * scale) for distance in row]
        for row in distance_matrix
    ]

    # Add a virtual end node. Zero-cost edges to it allow an open path.
    virtual_end = n
    costs.append([0] * (n + 1))

    for row in costs[:n]:
        row.append(0)

    manager = pywrapcp.RoutingIndexManager(
        n + 1,
        1,
        [start],
        [virtual_end],
    )
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index: int, to_index: int) -> int:
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return costs[from_node][to_node]

    callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )

    search_parameters.time_limit.seconds = time_limit_ms // 1000
    search_parameters.time_limit.nanos = (time_limit_ms % 1000) * 1_000_000

    solution = routing.SolveWithParameters(search_parameters)

    if solution is None:
        raise RuntimeError("OR-Tools could not find a route")

    route = []
    index = routing.Start(0)

    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)

        if node != virtual_end:
            route.append(node)

        index = solution.Value(routing.NextVar(index))

    return route
