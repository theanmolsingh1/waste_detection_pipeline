from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_alerts, routes_detection, routes_health, routes_statistics
from app.core.config import get_settings
from app.core.logging_config import configure_logging
from app.database.database import Base, engine
from app.services.detection_service import DetectionService

configure_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    app.state.settings = get_settings()
    app.state.detection_service = DetectionService()
    yield

app = FastAPI(title="Smart Water Waste Monitor", version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(routes_health.router, prefix="/api")
app.include_router(routes_detection.router, prefix="/api")
app.include_router(routes_alerts.router, prefix="/api")
app.include_router(routes_statistics.router, prefix="/api")
