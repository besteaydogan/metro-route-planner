import { Clock, GitBranch, Route as RouteIcon } from "lucide-react";
import { RouteResult } from "../types/route";
import { Station } from "../types/station";

type Props = {
  result: RouteResult | null;
  stations: Station[];
};

function stationName(stations: Station[], stationId: string): string {
  return stations.find((station) => station.id === stationId)?.name ?? stationId;
}

export function RouteResultPanel({ result, stations }: Props) {
  if (!result) {
    return (
      <section className="result-panel empty">
        <RouteIcon size={28} />
        <p>Rota sonucu burada gorunecek.</p>
      </section>
    );
  }

  return (
    <section className="result-panel">
      <div className="metrics">
        <div>
          <Clock size={20} />
          <strong>{result.totalDurationMinutes} dk</strong>
          <span>Toplam sure</span>
        </div>
        <div>
          <GitBranch size={20} />
          <strong>{result.transferCount}</strong>
          <span>Aktarma</span>
        </div>
        <div>
          <RouteIcon size={20} />
          <strong>{result.totalDistanceKm} km</strong>
          <span>Mesafe</span>
        </div>
      </div>

      <ol className="path-list">
        {result.path.map((stationId) => (
          <li key={stationId}>{stationName(stations, stationId)}</li>
        ))}
      </ol>

      <div className="segments">
        {result.segments.map((segment) => (
          <div key={`${segment.fromStationId}-${segment.toStationId}-${segment.lineId}`} className="segment">
            <span>{stationName(stations, segment.fromStationId)}</span>
            <span>{segment.lineId}</span>
            <span>{stationName(stations, segment.toStationId)}</span>
            <strong>{segment.durationMinutes} dk</strong>
          </div>
        ))}
      </div>
    </section>
  );
}
