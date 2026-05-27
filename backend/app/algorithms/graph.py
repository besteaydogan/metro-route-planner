from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    x: float
    y: float


@dataclass(frozen=True)
class StationNode:
    station_id: str
    name: str
    line_ids: tuple[str, ...]
    location: Location


@dataclass(frozen=True)
class Edge:
    to_station_id: str
    line_id: str
    duration_minutes: int
    distance_km: float


@dataclass(frozen=True)
class RouteSegment:
    from_station_id: str
    to_station_id: str
    line_id: str
    duration_minutes: int
    distance_km: float


@dataclass(frozen=True)
class RoutePlan:
    path: list[str]
    total_duration_minutes: int
    total_distance_km: float
    transfer_count: int
    segments: list[RouteSegment]


Graph = dict[str, list[Edge]]
