import heapq
from itertools import count

from app.algorithms.graph import Graph, RoutePlan
from app.algorithms.utils import build_plan, empty_plan


def find_balanced_route(
    graph: Graph,
    start_id: str,
    goal_id: str,
    transfer_penalty_minutes: int = 4,
) -> RoutePlan | None:
    if start_id == goal_id:
        return empty_plan(start_id)

    sequence = count()
    queue = [(0, 0, next(sequence), start_id, None, [])]
    best_score: dict[tuple[str, str | None], int] = {(start_id, None): 0}

    while queue:
        score, duration, _, station_id, current_line_id, path_edges = heapq.heappop(queue)
        if station_id == goal_id:
            return build_plan(path_edges)

        if score > best_score.get((station_id, current_line_id), 10**9):
            continue

        for edge in graph.get(station_id, []):
            transfer_cost = 0 if current_line_id in (None, edge.line_id) else transfer_penalty_minutes
            next_score = score + edge.duration_minutes + transfer_cost
            next_state = (edge.to_station_id, edge.line_id)
            if next_score < best_score.get(next_state, 10**9):
                best_score[next_state] = next_score
                heapq.heappush(
                    queue,
                    (
                        next_score,
                        duration + edge.duration_minutes,
                        next(sequence),
                        edge.to_station_id,
                        edge.line_id,
                        path_edges + [(station_id, edge)],
                    ),
                )

    return None
