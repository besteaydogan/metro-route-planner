import heapq
from itertools import count

from app.algorithms.graph import Graph, RoutePlan
from app.algorithms.utils import build_plan, empty_plan


def find_fastest_route(graph: Graph, start_id: str, goal_id: str) -> RoutePlan | None:
    if start_id == goal_id:
        return empty_plan(start_id)

    sequence = count()
    queue = [(0, 0, next(sequence), start_id, [])]
    best_duration: dict[str, int] = {start_id: 0}

    while queue:
        duration, stops, _, station_id, path_edges = heapq.heappop(queue)
        if station_id == goal_id:
            return build_plan(path_edges)

        if duration > best_duration.get(station_id, 10**9):
            continue

        for edge in graph.get(station_id, []):
            next_duration = duration + edge.duration_minutes
            if next_duration < best_duration.get(edge.to_station_id, 10**9):
                best_duration[edge.to_station_id] = next_duration
                heapq.heappush(
                    queue,
                    (
                        next_duration,
                        stops + 1,
                        next(sequence),
                        edge.to_station_id,
                        path_edges + [(station_id, edge)],
                    ),
                )

    return None
