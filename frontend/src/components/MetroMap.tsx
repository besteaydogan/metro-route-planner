import { Connection, Line, Station } from "../types/station";
import { RouteResult } from "../types/route";

type Props = {
  stations: Station[];
  connections: Connection[];
  lines: Line[];
  result: RouteResult | null;
};

function scale(value: number, min: number, max: number, size: number, padding: number): number {
  if (max === min) {
    return size / 2;
  }
  return padding + ((value - min) / (max - min)) * (size - padding * 2);
}

export function MetroMap({ stations, connections, lines, result }: Props) {
  const width = 720;
  const height = 420;
  const padding = 48;
  const xs = stations.map((station) => station.location.x);
  const ys = stations.map((station) => station.location.y);
  const minX = Math.min(...xs, 0);
  const maxX = Math.max(...xs, 1);
  const minY = Math.min(...ys, 0);
  const maxY = Math.max(...ys, 1);
  const routeEdges = new Set(result?.segments.map((segment) => `${segment.fromStationId}-${segment.toStationId}`) ?? []);

  const position = (stationId: string) => {
    const station = stations.find((item) => item.id === stationId);
    if (!station) {
      return { x: 0, y: 0 };
    }
    return {
      x: scale(station.location.x, minX, maxX, width, padding),
      y: height - scale(station.location.y, minY, maxY, height, padding)
    };
  };

  const lineColor = (lineId: string) => lines.find((line) => line.id === lineId)?.color ?? "#697386";

  return (
    <section className="map-panel" aria-label="Metro haritasi">
      <svg viewBox={`0 0 ${width} ${height}`} role="img">
        {connections.map((connection) => {
          const from = position(connection.fromStationId);
          const to = position(connection.toStationId);
          const selected =
            routeEdges.has(`${connection.fromStationId}-${connection.toStationId}`) ||
            routeEdges.has(`${connection.toStationId}-${connection.fromStationId}`);
          return (
            <line
              key={connection.id}
              x1={from.x}
              y1={from.y}
              x2={to.x}
              y2={to.y}
              stroke={lineColor(connection.lineId)}
              strokeWidth={selected ? 8 : 4}
              opacity={selected ? 1 : 0.36}
              strokeLinecap="round"
            />
          );
        })}
        {stations.map((station) => {
          const point = position(station.id);
          const selected = result?.path.includes(station.id) ?? false;
          return (
            <g key={station.id}>
              <circle cx={point.x} cy={point.y} r={selected ? 13 : 10} className={selected ? "station selected" : "station"} />
              <text x={point.x + 14} y={point.y - 12}>
                {station.name}
              </text>
            </g>
          );
        })}
      </svg>
    </section>
  );
}
