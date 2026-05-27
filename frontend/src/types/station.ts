export type Location = {
  x: number;
  y: number;
};

export type Station = {
  id: string;
  name: string;
  lineIds: string[];
  location: Location;
  isActive: boolean;
};

export type Line = {
  id: string;
  name: string;
  color: string;
};

export type Connection = {
  id: string;
  fromStationId: string;
  toStationId: string;
  lineId: string;
  durationMinutes: number;
  distanceKm: number;
  isActive: boolean;
};
