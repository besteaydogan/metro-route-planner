from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongodb import get_database
from app.schemas.station_schema import ConnectionSchema, LineSchema, StationSchema

router = APIRouter(prefix="/api", tags=["network"])


@router.get("/stations", response_model=list[StationSchema], response_model_by_alias=False)
async def list_stations(db: AsyncIOMotorDatabase = Depends(get_database)) -> list[dict]:
    return await db.stations.find({"isActive": True}).sort("_id", 1).to_list(length=None)


@router.get("/stations/{station_id}", response_model=StationSchema, response_model_by_alias=False)
async def get_station(station_id: str, db: AsyncIOMotorDatabase = Depends(get_database)) -> dict:
    station = await db.stations.find_one({"_id": station_id, "isActive": True})
    if station is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Station was not found")
    return station


@router.get("/lines", response_model=list[LineSchema], response_model_by_alias=False)
async def list_lines(db: AsyncIOMotorDatabase = Depends(get_database)) -> list[dict]:
    return await db.lines.find().sort("_id", 1).to_list(length=None)


@router.get("/connections", response_model=list[ConnectionSchema], response_model_by_alias=False)
async def list_connections(db: AsyncIOMotorDatabase = Depends(get_database)) -> list[dict]:
    return await db.connections.find({"isActive": True}).sort("_id", 1).to_list(length=None)
