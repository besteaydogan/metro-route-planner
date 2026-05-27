from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class RouteStrategy(StrEnum):
    MIN_TRANSFER = "MIN_TRANSFER"
    FASTEST = "FASTEST"
    FASTEST_HEURISTIC = "FASTEST_HEURISTIC"
    BALANCED = "BALANCED"


class RouteCalculateRequest(BaseModel):
    fromStationId: str
    toStationId: str
    strategy: RouteStrategy


class RouteSegmentSchema(BaseModel):
    fromStationId: str
    toStationId: str
    lineId: str
    durationMinutes: int
    distanceKm: float


class RouteCalculateResponse(BaseModel):
    strategy: RouteStrategy
    path: list[str]
    totalDurationMinutes: int
    totalDistanceKm: float
    transferCount: int
    segments: list[RouteSegmentSchema]


class RouteHistoryItem(RouteCalculateResponse):
    id: str
    fromStationId: str
    toStationId: str
    createdAt: datetime
