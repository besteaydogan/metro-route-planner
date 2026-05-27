from app.algorithms.graph import Edge, RoutePlan, RouteSegment


def build_plan(path_edges: list[tuple[str, Edge]]) -> RoutePlan:
    if not path_edges:
        return RoutePlan(path=[], total_duration_minutes=0, total_distance_km=0, transfer_count=0, segments=[])

    path = [path_edges[0][0]]
    segments: list[RouteSegment] = []
    previous_line_id: str | None = None
    transfer_count = 0
    total_duration = 0
    total_distance = 0.0

    for from_station_id, edge in path_edges:
        if previous_line_id is not None and previous_line_id != edge.line_id:
            transfer_count += 1
        previous_line_id = edge.line_id
        path.append(edge.to_station_id)
        total_duration += edge.duration_minutes
        total_distance += edge.distance_km
        segments.append(
            RouteSegment(
                from_station_id=from_station_id,
                to_station_id=edge.to_station_id,
                line_id=edge.line_id,
                duration_minutes=edge.duration_minutes,
                distance_km=edge.distance_km,
            )
        )

    return RoutePlan(
        path=path,
        total_duration_minutes=total_duration,
        total_distance_km=round(total_distance, 2),
        transfer_count=transfer_count,
        segments=segments,
    )


def empty_plan(station_id: str) -> RoutePlan:
    return RoutePlan(path=[station_id], total_duration_minutes=0, total_distance_km=0, transfer_count=0, segments=[])
