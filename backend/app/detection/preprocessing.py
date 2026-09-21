import cv2
import numpy as np


class FramePreprocessor:
    """Optional diagnostic preprocessing. YOLO receives the original BGR frame by default.

    The preview pipeline resizes to 224x224, converts BGR to RGB, applies Gaussian blur,
    and normalizes to 0..1. Passing that preview to YOLO is disabled because Ultralytics
    performs its own letterboxing/normalization and needs original geometry for boxes.
    """
    def __init__(self, size: tuple[int, int] = (224, 224)):
        self.size = size

    def prepare_preview(self, frame: np.ndarray) -> np.ndarray:
        if frame is None or frame.size == 0:
            raise ValueError("Invalid frame")
        resized = cv2.resize(frame, self.size, interpolation=cv2.INTER_AREA)
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        blurred = cv2.GaussianBlur(rgb, (3, 3), 0)
        return blurred.astype(np.float32) / 255.0

    def for_inference(self, frame: np.ndarray) -> np.ndarray:
        if frame is None or frame.size == 0:
            raise ValueError("Invalid frame")
        return frame
