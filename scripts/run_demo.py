"""Process a generated demo frame through the full local pipeline."""
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
frame = np.zeros((480, 640, 3), dtype=np.uint8)
frame[:] = (80, 120, 100)
result = service.process_frame(frame)
print("DEMO/MOCK RESULT (uses a synthetic detection only if no custom model is supplied):")
print(result)
