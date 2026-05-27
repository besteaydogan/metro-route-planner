import heapq
from itertools import count

from app.algorithms.graph import Graph, RoutePlan
from app.algorithms.utils import build_plan, empty_plan


def find_min_transfer_route(graph: Graph, start_id: str, goal_id: str) -> RoutePlan | None:
    if start_id == goal_id:
        return empty_plan(start_id)

    sequence = count()
    queue = [(0, 0, 0, next(sequence), start_id, None, [])]
    best: dict[tuple[str, str | None], tuple[int, int, int]] = {(start_id, None): (0, 0, 0)}

    while queue:
        transfers, stops, duration, _, station_id, current_line_id, path_edges = heapq.heappop(queue)
        if station_id == goal_id:
            return build_plan(path_edges)

        for edge in graph.get(station_id, []):
            transfer_cost = 0 if current_line_id in (None, edge.line_id) else 1
            next_state = (edge.to_station_id, edge.line_id)
            next_score = (transfers + transfer_cost, stops + 1, duration + edge.duration_minutes)
            if next_score < best.get(next_state, (10**9, 10**9, 10**9)):
                best[next_state] = next_score
                heapq.heappush(
                    queue,
                    (
                        next_score[0],
                        next_score[1],
                        next_score[2],
                        next(sequence),
                        edge.to_station_id,
                        edge.line_id,
                        path_edges + [(station_id, edge)],
                    ),
                )

    return None
