import logging
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
import cv2
import numpy as np
from app.alerts.alert_service import AlertService
from app.core.config import get_settings
from app.database.database import SessionLocal
from app.database.repository import create_detection
from app.detection.detector import WasteDetector
from app.detection.postprocessing import filter_by_confidence
from app.detection.preprocessing import FramePreprocessor
from app.gps.mock_gps import MockGPS
from app.gps.serial_gps import SerialGPS

logger = logging.getLogger(__name__)


class DetectionService:
    def __init__(self):
        self.settings = get_settings()
        self.preprocessor = FramePreprocessor()
        self.detector = WasteDetector()
        self.gps = SerialGPS() if self.settings.gps_mode == "serial" else MockGPS()
        self.alerts = AlertService()
        self.last_alerts: dict[str, float] = {}
        self.inference_times, self.processing_times, self.alert_latencies = deque(maxlen=300), deque(maxlen=300), deque(maxlen=300)
        self.processed_frames = 0
        Path(self.settings.detection_image_dir).mkdir(parents=True, exist_ok=True)

    def _is_duplicate(self, detection: dict) -> bool:
        x1, y1, x2, y2 = detection["bbox"]
        key = f"{detection['class_name']}:{round((x1+x2)/2/100)}:{round((y1+y2)/2/100)}"
        now = time.monotonic()
        last = self.last_alerts.get(key)
        if last is not None and now - last < self.settings.alert_cooldown_seconds:
            return True
        self.last_alerts[key] = now
        return False

    def _save_image(self, frame: np.ndarray, stamp: datetime) -> str | None:
        path = Path(self.settings.detection_image_dir) / f"detection_{stamp.strftime('%Y%m%d_%H%M%S_%f')}.jpg"
        return str(path) if cv2.imwrite(str(path), frame) else None

    def process_frame(self, frame: np.ndarray) -> dict:
        started = time.perf_counter()
        model_frame = self.preprocessor.for_inference(frame)
        infer_started = time.perf_counter()
        raw = self.detector.detect(model_frame)
        self.inference_times.append(time.perf_counter() - infer_started)
        valid = filter_by_confidence(raw, self.settings.confidence_threshold)
        results = []
        for detection in valid:
            if self._is_duplicate(detection):
                continue
            stamp = datetime.now(timezone.utc)
            location = self.gps.get_location()
            item = {
                "waste_type": detection["class_name"], "confidence": detection["confidence"],
                **location, "timestamp": stamp, "status": "confirmed", "is_demo": detection.get("is_demo", False),
            }
            item["image_path"] = self._save_image(frame, stamp)
            alert_started = time.perf_counter()
            item["alert_sent"] = self.alerts.send_alert(item)
            self.alert_latencies.append(time.perf_counter() - alert_started)
            try:
                with SessionLocal() as db:
                    stored = create_detection(db, **item)
                item["id"] = stored.id
            except Exception as exc:
                logger.exception("Detection database storage failed: %s", exc)
                item["storage_error"] = "Database unavailable; detection was not persisted"
            item["timestamp"] = stamp.isoformat()
            results.append(item)
        self.processed_frames += 1
        self.processing_times.append(time.perf_counter() - started)
        return {"detections": results, "raw_detection_count": len(raw), "demo_mode": self.detector.demo_mode and not self.detector.available}

    def metrics(self) -> dict:
        avg = lambda values: round(sum(values) / len(values) * 1000, 2) if values else 0
        total_time = sum(self.processing_times)
        return {"average_inference_ms": avg(self.inference_times), "average_processing_ms": avg(self.processing_times), "average_alert_latency_ms": avg(self.alert_latencies), "fps": round(len(self.processing_times) / total_time, 2) if total_time else 0, "processed_frames": self.processed_frames}

    def annotate(self, frame: np.ndarray) -> np.ndarray:
        raw = self.detector.detect(frame)
        for d in filter_by_confidence(raw, self.settings.confidence_threshold):
            x1, y1, x2, y2 = map(int, d["bbox"])
            label = f"{d['class_name'].replace('_', ' ').title()} {d['confidence']:.0%}" + (" (DEMO)" if d.get("is_demo") else "")
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 215, 255), 2)
            cv2.putText(frame, label, (x1, max(25, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, .55, (0, 215, 255), 2)
        return frame
