import { apiRequest } from "./client";
import { Connection, Line, Station } from "../types/station";

export function fetchStations(): Promise<Station[]> {
  return apiRequest<Station[]>("/api/stations");
}

export function fetchLines(): Promise<Line[]> {
  return apiRequest<Line[]>("/api/lines");
}

export function fetchConnections(): Promise<Connection[]> {
  return apiRequest<Connection[]>("/api/connections");
}
