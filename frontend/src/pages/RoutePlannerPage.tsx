import { Loader2, Navigation } from "lucide-react";
import { FormEvent, useEffect, useMemo, useState } from "react";
import { calculateRoute } from "../api/routeApi";
import { fetchConnections, fetchLines, fetchStations } from "../api/stationApi";
import { MetroMap } from "../components/MetroMap";
import { RouteResultPanel } from "../components/RouteResultPanel";
import { StationSelect } from "../components/StationSelect";
import { StrategySelector } from "../components/StrategySelector";
import { RouteResult, RouteStrategy } from "../types/route";
import { Connection, Line, Station } from "../types/station";

export function RoutePlannerPage() {
  const [stations, setStations] = useState<Station[]>([]);
  const [connections, setConnections] = useState<Connection[]>([]);
  const [lines, setLines] = useState<Line[]>([]);
  const [fromStationId, setFromStationId] = useState("");
  const [toStationId, setToStationId] = useState("");
  const [strategy, setStrategy] = useState<RouteStrategy>("FASTEST");
  const [result, setResult] = useState<RouteResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([fetchStations(), fetchConnections(), fetchLines()])
      .then(([stationData, connectionData, lineData]) => {
        setStations(stationData);
        setConnections(connectionData);
        setLines(lineData);
        setFromStationId(stationData[0]?.id ?? "");
        setToStationId(stationData[stationData.length - 1]?.id ?? "");
      })
      .catch((err: Error) => setError(err.message));
  }, []);

  const canSubmit = useMemo(
    () => Boolean(fromStationId && toStationId && fromStationId !== toStationId && !isLoading),
    [fromStationId, isLoading, toStationId]
  );

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canSubmit) {
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const route = await calculateRoute(fromStationId, toStationId, strategy);
      setResult(route);
    } catch (err) {
      setResult(null);
      setError(err instanceof Error ? err.message : "Rota hesaplanamadi");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="page">
      <header className="topbar">
        <div>
          <p>FastAPI + MongoDB + React</p>
          <h1>MetroRoute Planner</h1>
        </div>
        <span className="status">Docker-ready MVP</span>
      </header>

      <section className="workspace">
        <form className="planner-panel" onSubmit={handleSubmit}>
          <StationSelect id="from" label="Baslangic" value={fromStationId} stations={stations} onChange={setFromStationId} />
          <StationSelect id="to" label="Hedef" value={toStationId} stations={stations} onChange={setToStationId} />
          <StrategySelector value={strategy} onChange={setStrategy} />

          {fromStationId === toStationId && <p className="notice">Baslangic ve hedef farkli olmali.</p>}
          {error && <p className="error">{error}</p>}

          <button className="submit-button" type="submit" disabled={!canSubmit}>
            {isLoading ? <Loader2 className="spin" size={18} /> : <Navigation size={18} />}
            <span>Rota Hesapla</span>
          </button>
        </form>

        <RouteResultPanel result={result} stations={stations} />
      </section>

      <MetroMap stations={stations} connections={connections} lines={lines} result={result} />
    </main>
  );
}
