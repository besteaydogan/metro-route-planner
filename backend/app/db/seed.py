from motor.motor_asyncio import AsyncIOMotorDatabase


LINES = [
    {"_id": "M1", "name": "Kirmizi Hat", "color": "#d93f3f"},
    {"_id": "M2", "name": "Mavi Hat", "color": "#276ef1"},
    {"_id": "M3", "name": "Yesil Hat", "color": "#2a9d55"},
]

STATIONS = [
    {"_id": "A", "name": "Aksaray", "lineIds": ["M1", "M2"], "location": {"x": 0, "y": 0}, "isActive": True},
    {"_id": "B", "name": "Bahcelievler", "lineIds": ["M1"], "location": {"x": 2, "y": 1}, "isActive": True},
    {"_id": "C", "name": "Cevizlibag", "lineIds": ["M1"], "location": {"x": 5, "y": 1}, "isActive": True},
    {"_id": "D", "name": "Demirkapi", "lineIds": ["M2"], "location": {"x": 3, "y": 4}, "isActive": True},
    {"_id": "E", "name": "Esenler", "lineIds": ["M2", "M3"], "location": {"x": 6, "y": 5}, "isActive": True},
    {"_id": "F", "name": "Fenertepe", "lineIds": ["M3"], "location": {"x": 9, "y": 6}, "isActive": True},
    {"_id": "G", "name": "Goztepe", "lineIds": ["M3"], "location": {"x": 10, "y": 2}, "isActive": True},
]

CONNECTIONS = [
    {"_id": "conn_A_B", "fromStationId": "A", "toStationId": "B", "lineId": "M1", "durationMinutes": 2, "distanceKm": 1.2, "isActive": True},
    {"_id": "conn_B_C", "fromStationId": "B", "toStationId": "C", "lineId": "M1", "durationMinutes": 3, "distanceKm": 1.8, "isActive": True},
    {"_id": "conn_A_D", "fromStationId": "A", "toStationId": "D", "lineId": "M2", "durationMinutes": 5, "distanceKm": 2.1, "isActive": True},
    {"_id": "conn_D_E", "fromStationId": "D", "toStationId": "E", "lineId": "M2", "durationMinutes": 2, "distanceKm": 1.1, "isActive": True},
    {"_id": "conn_E_F", "fromStationId": "E", "toStationId": "F", "lineId": "M3", "durationMinutes": 6, "distanceKm": 3.0, "isActive": True},
    {"_id": "conn_C_G", "fromStationId": "C", "toStationId": "G", "lineId": "M3", "durationMinutes": 9, "distanceKm": 4.4, "isActive": True},
    {"_id": "conn_G_F", "fromStationId": "G", "toStationId": "F", "lineId": "M3", "durationMinutes": 3, "distanceKm": 1.3, "isActive": True},
]


async def seed_demo_data(db: AsyncIOMotorDatabase) -> None:
    for collection_name, documents in (
        ("lines", LINES),
        ("stations", STATIONS),
        ("connections", CONNECTIONS),
    ):
        collection = db[collection_name]
        for document in documents:
            await collection.replace_one({"_id": document["_id"]}, document, upsert=True)
