from fastapi import APIRouter, Request
from app.database.database import SessionLocal
from app.database.repository import statistics

router = APIRouter(tags=["statistics"])

@router.get("/statistics")
def get_statistics():
    with SessionLocal() as db:
        return statistics(db)

@router.get("/statistics/performance")
def performance(request: Request):
    return request.app.state.detection_service.metrics()
