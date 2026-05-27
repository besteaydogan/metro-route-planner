import { apiRequest } from "./client";
import { RouteResult, RouteStrategy } from "../types/route";

export function calculateRoute(
  fromStationId: string,
  toStationId: string,
  strategy: RouteStrategy
): Promise<RouteResult> {
  return apiRequest<RouteResult>("/api/routes/calculate", {
    method: "POST",
    body: JSON.stringify({ fromStationId, toStationId, strategy })
  });
}
