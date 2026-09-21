import sys
import os
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
os.chdir(ROOT / "backend")
from app.database.database import Base, engine
from app.services.detection_service import DetectionService

Base.metadata.create_all(engine)
service = DetectionService()
for _ in range(3):
    service.last_alerts.clear()
    print(service.process_frame(np.zeros((480, 640, 3), dtype=np.uint8)))
