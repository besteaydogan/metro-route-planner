from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongodb import get_database
from app.schemas.route_schema import RouteCalculateRequest, RouteCalculateResponse, RouteHistoryItem
from app.services.route_planner_service import calculate_route

router = APIRouter(prefix="/api/routes", tags=["routes"])


@router.post("/calculate", response_model=RouteCalculateResponse)
async def calculate(
    request: RouteCalculateRequest,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> RouteCalculateResponse:
    return await calculate_route(db, request)


@router.get("/history", response_model=list[RouteHistoryItem])
async def list_history(db: AsyncIOMotorDatabase = Depends(get_database)) -> list[dict]:
    documents = await db.route_search_history.find().sort("createdAt", -1).limit(20).to_list(length=20)
    for document in documents:
        document["id"] = str(document.pop("_id"))
    return documents
