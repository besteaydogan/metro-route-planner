import { RouteStrategy } from "../types/route";

const strategies: Array<{ value: RouteStrategy; label: string; description: string }> = [
  { value: "MIN_TRANSFER", label: "Min Aktarma", description: "Hat degisimini azaltir" },
  { value: "FASTEST", label: "En Hizli", description: "Dijkstra ile sureyi azaltir" },
  { value: "FASTEST_HEURISTIC", label: "A*", description: "Hedefe yonlu arama yapar" },
  { value: "BALANCED", label: "Dengeli", description: "Sure + aktarma cezasini dengeler" }
];

type Props = {
  value: RouteStrategy;
  onChange: (strategy: RouteStrategy) => void;
};

export function StrategySelector({ value, onChange }: Props) {
  return (
    <div className="strategy-group" role="radiogroup" aria-label="Rota stratejisi">
      {strategies.map((strategy) => (
        <button
          key={strategy.value}
          type="button"
          className={strategy.value === value ? "strategy active" : "strategy"}
          onClick={() => onChange(strategy.value)}
          title={strategy.description}
        >
          <strong>{strategy.label}</strong>
          <span>{strategy.description}</span>
        </button>
      ))}
    </div>
  );
}
