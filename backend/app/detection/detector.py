import logging
import os
from pathlib import Path
import numpy as np
from app.core.config import get_settings

logger = logging.getLogger(__name__)
WASTE_CLASSES = {"plastic_bottle", "plastic_bag", "aluminium_can", "general_debris"}


class WasteDetector:
    def __init__(self, model_path: str | None = None, demo_mode: bool | None = None):
        settings = get_settings()
        self.model_path = Path(model_path or settings.model_path)
        self.demo_mode = settings.demo_mode if demo_mode is None else demo_mode
        self.model = None
        self.available = False
        self.load_error = None
        self._load()

    def _load(self):
        if not self.model_path.exists():
            self.load_error = f"Custom waste model missing: {self.model_path}"
            logger.warning("%s; %s", self.load_error, "demo detections enabled" if self.demo_mode else "inference disabled")
            return
        try:
            # Keep Ultralytics' settings/cache writable in restricted VS Code environments.
            os.environ.setdefault("YOLO_CONFIG_DIR", str(Path.cwd()))
            from ultralytics import YOLO
            self.model = YOLO(str(self.model_path))
            self.available = True
            logger.info("YOLO model loaded: %s", self.model_path)
        except Exception as exc:
            self.load_error = f"Model loading failed: {exc}"
            logger.exception(self.load_error)

    def detect(self, frame: np.ndarray) -> list[dict]:
        if frame is None or frame.size == 0:
            raise ValueError("Invalid frame")
        if self.available:
            result = self.model(frame, verbose=False)[0]
            names = result.names
            output = []
            for box in result.boxes:
                class_name = str(names[int(box.cls[0])]).lower().replace(" ", "_")
                if class_name in WASTE_CLASSES:
                    output.append({"class_name": class_name, "confidence": round(float(box.conf[0]), 4), "bbox": [round(float(v), 1) for v in box.xyxy[0].tolist()], "is_demo": False})
            return output
        if self.demo_mode:
            h, w = frame.shape[:2]
            return [{"class_name": "plastic_bottle", "confidence": 0.97, "bbox": [w * .3, h * .2, w * .6, h * .8], "is_demo": True}]
        return []
