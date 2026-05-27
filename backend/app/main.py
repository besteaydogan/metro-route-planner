from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.route_routes import router as route_router
from app.api.routes.station_routes import router as station_router
from app.config import get_settings
from app.db.mongodb import close_mongo_connection, connect_to_mongo, get_database
from app.db.seed import seed_demo_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    await seed_demo_data(get_database())
    yield
    await close_mongo_connection()


app = FastAPI(
    title="MetroRoute Planner API",
    description="Route optimization API with BFS, Dijkstra and A* strategies.",
    version="1.0.0",
    lifespan=lifespan,
)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(station_router)
app.include_router(route_router)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
