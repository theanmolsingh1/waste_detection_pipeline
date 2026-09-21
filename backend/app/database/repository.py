from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.database.models import Detection


def create_detection(db: Session, **values) -> Detection:
    item = Detection(**values)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_detections(db: Session, limit: int = 100) -> list[Detection]:
    return list(db.scalars(select(Detection).order_by(Detection.timestamp.desc()).limit(limit)))


def get_detection(db: Session, detection_id: int) -> Detection | None:
    return db.get(Detection, detection_id)


def statistics(db: Session) -> dict:
    rows = db.execute(select(Detection.waste_type, func.count(Detection.id)).group_by(Detection.waste_type)).all()
    counts = dict(rows)
    return {
        "total_detections": sum(counts.values()),
        "plastic_bottles": counts.get("plastic_bottle", 0),
        "plastic_bags": counts.get("plastic_bag", 0),
        "aluminium_cans": counts.get("aluminium_can", 0),
        "general_debris": counts.get("general_debris", 0),
    }
