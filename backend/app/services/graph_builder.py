from motor.motor_asyncio import AsyncIOMotorDatabase

from app.algorithms.graph import Edge, Graph, Location, StationNode


async def build_graph(db: AsyncIOMotorDatabase) -> tuple[Graph, dict[str, StationNode]]:
    station_documents = await db.stations.find({"isActive": True}).to_list(length=None)
    connection_documents = await db.connections.find({"isActive": True}).to_list(length=None)

    stations = {
        document["_id"]: StationNode(
            station_id=document["_id"],
            name=document["name"],
            line_ids=tuple(document.get("lineIds", [])),
            location=Location(
                x=float(document.get("location", {}).get("x", 0)),
                y=float(document.get("location", {}).get("y", 0)),
            ),
        )
        for document in station_documents
    }

    graph: Graph = {station_id: [] for station_id in stations}
    for document in connection_documents:
        from_station_id = document["fromStationId"]
        to_station_id = document["toStationId"]
        if from_station_id not in stations or to_station_id not in stations:
            continue

        edge = Edge(
            to_station_id=to_station_id,
            line_id=document["lineId"],
            duration_minutes=int(document["durationMinutes"]),
            distance_km=float(document["distanceKm"]),
        )
        reverse_edge = Edge(
            to_station_id=from_station_id,
            line_id=document["lineId"],
            duration_minutes=int(document["durationMinutes"]),
            distance_km=float(document["distanceKm"]),
        )
        graph[from_station_id].append(edge)
        graph[to_station_id].append(reverse_edge)

    return graph, stations
