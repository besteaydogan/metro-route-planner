from datetime import UTC, datetime

from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.algorithms.astar import find_fastest_route_with_heuristic
from app.algorithms.balanced import find_balanced_route
from app.algorithms.bfs import find_min_transfer_route
from app.algorithms.dijkstra import find_fastest_route
from app.algorithms.graph import RoutePlan
from app.schemas.route_schema import (
    RouteCalculateRequest,
    RouteCalculateResponse,
    RouteSegmentSchema,
    RouteStrategy,
)
from app.services.graph_builder import build_graph


def _to_response(strategy: RouteStrategy, plan: RoutePlan) -> RouteCalculateResponse:
    return RouteCalculateResponse(
        strategy=strategy,
        path=plan.path,
        totalDurationMinutes=plan.total_duration_minutes,
        totalDistanceKm=plan.total_distance_km,
        transferCount=plan.transfer_count,
        segments=[
            RouteSegmentSchema(
                fromStationId=segment.from_station_id,
                toStationId=segment.to_station_id,
                lineId=segment.line_id,
                durationMinutes=segment.duration_minutes,
                distanceKm=segment.distance_km,
            )
            for segment in plan.segments
        ],
    )


async def calculate_route(
    db: AsyncIOMotorDatabase,
    request: RouteCalculateRequest,
    save_history: bool = True,
) -> RouteCalculateResponse:
    graph, stations = await build_graph(db)
    if request.fromStationId not in stations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Start station was not found")
    if request.toStationId not in stations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target station was not found")

    if request.strategy == RouteStrategy.MIN_TRANSFER:
        plan = find_min_transfer_route(graph, request.fromStationId, request.toStationId)
    elif request.strategy == RouteStrategy.FASTEST:
        plan = find_fastest_route(graph, request.fromStationId, request.toStationId)
    elif request.strategy == RouteStrategy.FASTEST_HEURISTIC:
        plan = find_fastest_route_with_heuristic(graph, stations, request.fromStationId, request.toStationId)
    else:
        plan = find_balanced_route(graph, request.fromStationId, request.toStationId)

    if plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No route exists between these stations")

    response = _to_response(request.strategy, plan)
    if save_history:
        history_document = response.model_dump(mode="json")
        history_document.update(
            {
                "fromStationId": request.fromStationId,
                "toStationId": request.toStationId,
                "createdAt": datetime.now(UTC),
            }
        )
        await db.route_search_history.insert_one(history_document)

    return response
