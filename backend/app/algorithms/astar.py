import heapq
from itertools import count

from app.algorithms.graph import Graph, RoutePlan, StationNode
from app.algorithms.utils import build_plan, empty_plan


def _heuristic(stations: dict[str, StationNode], station_id: str, goal_id: str) -> float:
    current = stations[station_id].location
    goal = stations[goal_id].location
    return 0.1 * (abs(current.x - goal.x) + abs(current.y - goal.y))


def find_fastest_route_with_heuristic(
    graph: Graph,
    stations: dict[str, StationNode],
    start_id: str,
    goal_id: str,
) -> RoutePlan | None:
    if start_id == goal_id:
        return empty_plan(start_id)

    sequence = count()
    queue = [(_heuristic(stations, start_id, goal_id), 0, next(sequence), start_id, [])]
    best_duration: dict[str, int] = {start_id: 0}

    while queue:
        _, duration, _, station_id, path_edges = heapq.heappop(queue)
        if station_id == goal_id:
            return build_plan(path_edges)

        if duration > best_duration.get(station_id, 10**9):
            continue

        for edge in graph.get(station_id, []):
            next_duration = duration + edge.duration_minutes
            if next_duration < best_duration.get(edge.to_station_id, 10**9):
                best_duration[edge.to_station_id] = next_duration
                priority = next_duration + _heuristic(stations, edge.to_station_id, goal_id)
                heapq.heappush(
                    queue,
                    (
                        priority,
                        next_duration,
                        next(sequence),
                        edge.to_station_id,
                        path_edges + [(station_id, edge)],
                    ),
                )

    return None
