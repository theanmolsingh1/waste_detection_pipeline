import logging
import time
import cv2
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from app.database.database import SessionLocal
from app.database.repository import get_detection, list_detections
from app.detection.camera import CameraSource

logger = logging.getLogger(__name__)
router = APIRouter(tags=["detections"])

def serialize(item):
    return {"id": item.id, "waste_type": item.waste_type, "confidence": item.confidence, "latitude": item.latitude, "longitude": item.longitude, "timestamp": item.timestamp.isoformat(), "image_path": item.image_path, "status": item.status, "alert_sent": item.alert_sent, "is_demo": item.is_demo}

@router.get("/detections")
def detections(limit: int = 100):
    with SessionLocal() as db:
        return [serialize(x) for x in list_detections(db, max(1, min(limit, 500)))]

@router.get("/detections/{detection_id}")
def detection_by_id(detection_id: int):
    with SessionLocal() as db:
        item = get_detection(db, detection_id)
        if not item: raise HTTPException(404, "Detection not found")
        return serialize(item)

@router.post("/detection/process")
async def process_uploaded_frame(request: Request):
    body = await request.body()
    if not body: raise HTTPException(400, "JPEG/PNG image bytes required in request body")
    image = cv2.imdecode(__import__('numpy').frombuffer(body, __import__('numpy').uint8), cv2.IMREAD_COLOR)
    if image is None: raise HTTPException(400, "Invalid image bytes")
    return request.app.state.detection_service.process_frame(image)

def _stream(app):
    source = CameraSource(app.state.settings.camera_value)
    try:
        source.start()
        logger.info("Camera started")
        while True:
            ok, frame = source.read()
            if not ok: break
            app.state.detection_service.process_frame(frame)
            annotated = app.state.detection_service.annotate(frame)
            ok, encoded = cv2.imencode(".jpg", annotated)
            if ok: yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + encoded.tobytes() + b"\r\n"
            time.sleep(.03)
    except Exception as exc:
        logger.error("Camera stream unavailable: %s", exc)
    finally:
        source.release()

@router.get("/camera/stream")
def camera_stream(request: Request):
    return StreamingResponse(_stream(request.app), media_type="multipart/x-mixed-replace; boundary=frame")
