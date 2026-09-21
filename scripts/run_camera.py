"""Run webcam processing; Ctrl+C to stop."""
import sys
import os
from pathlib import Path
import cv2
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
os.chdir(ROOT / "backend")
from app.database.database import Base, engine
from app.detection.camera import CameraSource
from app.services.detection_service import DetectionService

Base.metadata.create_all(engine)
service, camera = DetectionService(), CameraSource(0).start()
try:
    while True:
        ok, frame = camera.read()
        if not ok: break
        print(service.process_frame(frame))
        cv2.imshow("Smart Waste Monitor", service.annotate(frame))
        if cv2.waitKey(1) & 0xFF == ord("q"): break
finally:
    camera.release(); cv2.destroyAllWindows()
