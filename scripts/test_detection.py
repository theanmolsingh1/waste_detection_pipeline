"""Run a self-contained detector smoke test from the project root."""
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
from app.detection.detector import WasteDetector

frame = np.zeros((480, 640, 3), dtype=np.uint8)
detector = WasteDetector()
detections = detector.detect(frame)
print({"model_available": detector.available, "load_message": detector.load_error, "detections": detections})
assert all({"class_name", "confidence", "bbox"} <= d.keys() for d in detections)
