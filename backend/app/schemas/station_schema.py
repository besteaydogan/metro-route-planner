from pydantic import BaseModel, Field


class LocationSchema(BaseModel):
    x: float
    y: float


class StationSchema(BaseModel):
    id: str = Field(alias="_id")
    name: str
    lineIds: list[str]
    location: LocationSchema
    isActive: bool

    model_config = {"populate_by_name": True}


class LineSchema(BaseModel):
    id: str = Field(alias="_id")
    name: str
    color: str

    model_config = {"populate_by_name": True}


class ConnectionSchema(BaseModel):
    id: str = Field(alias="_id")
    fromStationId: str
    toStationId: str
    lineId: str
    durationMinutes: int
    distanceKm: float
    isActive: bool

    model_config = {"populate_by_name": True}
