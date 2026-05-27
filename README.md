# MetroRoute Planner

MetroRoute Planner, tek dosyalik Python metro simülasyonunu full-stack bir rota optimizasyon ürününe dönüştüren portfolyo projesidir. Uygulama FastAPI, MongoDB, React TypeScript ve Docker Compose ile çalışır.

## Özellikler

- Demo metro ağı MongoDB'ye otomatik seed edilir.
- `MIN_TRANSFER` stratejisi hat değişimini azaltan BFS tabanlı rota bulur.
- `FASTEST` stratejisi Dijkstra ile en kısa süreli rotayı hesaplar.
- `FASTEST_HEURISTIC` stratejisi A* ile hedefe yönlü arama yapar.
- React arayüzünde başlangıç, hedef ve strateji seçilerek rota sonucu görüntülenir.
- Tek komutla backend, frontend, MongoDB ve mongo-express ayağa kalkar.

## Teknoloji Stack

- Backend: FastAPI, Motor, Pydantic
- Database: MongoDB
- Frontend: React, TypeScript, Vite, lucide-react
- Container: Docker Compose
- Algorithms: BFS, Dijkstra, A*

## Çalıştırma

```bash
docker compose up --build
```

Servisler:

- Frontend: http://localhost:5173
- FastAPI Swagger: http://localhost:8000/docs
- Mongo Express: http://localhost:8081
- MongoDB: localhost:27017

## API

| Endpoint | Method | Açıklama |
| --- | --- | --- |
| `/health` | GET | Backend sağlık kontrolü |
| `/api/stations` | GET | Aktif istasyonları listeler |
| `/api/stations/{station_id}` | GET | Tek istasyon detayını döner |
| `/api/lines` | GET | Metro hatlarını listeler |
| `/api/connections` | GET | İstasyon bağlantılarını listeler |
| `/api/routes/calculate` | POST | Seçilen stratejiye göre rota hesaplar |
| `/api/routes/history` | GET | Son rota aramalarını listeler |

Örnek route request:

```json
{
  "fromStationId": "A",
  "toStationId": "F",
  "strategy": "FASTEST"
}
```

Örnek response:

```json
{
  "strategy": "FASTEST",
  "path": ["A", "D", "E", "F"],
  "totalDurationMinutes": 13,
  "totalDistanceKm": 6.2,
  "transferCount": 1,
  "segments": [
    { "fromStationId": "A", "toStationId": "D", "lineId": "M2", "durationMinutes": 5, "distanceKm": 2.1 },
    { "fromStationId": "D", "toStationId": "E", "lineId": "M2", "durationMinutes": 2, "distanceKm": 1.1 },
    { "fromStationId": "E", "toStationId": "F", "lineId": "M3", "durationMinutes": 6, "distanceKm": 3.0 }
  ]
}
```

## Lokal Backend Testleri

Backend bağımlılıkları kurulduktan sonra:

```bash
cd backend
pytest
```

## Lokal Frontend

Frontend pnpm ile çalışır:

```bash
cd frontend
pnpm install
pnpm dev
```

## Öğrenme Notları

- Graph modelinde istasyonlar node, bağlantılar edge, süre/mesafe/hat bilgisi weight olarak düşünülür.
- BFS ağırlıkları değil geçiş/aktarma mantığını takip eder.
- Dijkstra ağırlıklı graf üzerinde en düşük toplam süreyi bulur.
- A* `g(n) + h(n)` formülüyle Dijkstra'ya hedef tahmini ekler.

Eski bootcamp simülasyonu referans olarak `BesteAydogan_MetroSimulation.py` içinde korunmuştur.
