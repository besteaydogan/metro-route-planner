export type RouteStrategy = "MIN_TRANSFER" | "FASTEST" | "FASTEST_HEURISTIC" | "BALANCED";

export type RouteSegment = {
  fromStationId: string;
  toStationId: string;
  lineId: string;
  durationMinutes: number;
  distanceKm: number;
};

export type RouteResult = {
  strategy: RouteStrategy;
  path: string[];
  totalDurationMinutes: number;
  totalDistanceKm: number;
  transferCount: number;
  segments: RouteSegment[];
};
