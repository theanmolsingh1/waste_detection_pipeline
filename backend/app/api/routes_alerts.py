from fastapi import APIRouter
from app.database.database import SessionLocal
from app.database.repository import list_detections
from app.api.routes_detection import serialize

router = APIRouter(tags=["alerts"])

@router.get("/alerts")
def alerts(limit: int = 100):
    with SessionLocal() as db:
        return [serialize(d) for d in list_detections(db, limit) if d.alert_sent]
