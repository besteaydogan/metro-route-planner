import { Station } from "../types/station";

type Props = {
  id: string;
  label: string;
  value: string;
  stations: Station[];
  onChange: (stationId: string) => void;
};

export function StationSelect({ id, label, value, stations, onChange }: Props) {
  return (
    <label className="field" htmlFor={id}>
      <span>{label}</span>
      <select id={id} value={value} onChange={(event) => onChange(event.target.value)}>
        <option value="">Istasyon sec</option>
        {stations.map((station) => (
          <option key={station.id} value={station.id}>
            {station.name} ({station.id})
          </option>
        ))}
      </select>
    </label>
  );
}
