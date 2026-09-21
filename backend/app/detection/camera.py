import cv2


class CameraSource:
    def __init__(self, source=0):
        self.source = source
        self.capture = None

    def start(self):
        self.capture = cv2.VideoCapture(self.source)
        if not self.capture.isOpened():
            self.capture.release()
            self.capture = None
            raise RuntimeError(f"Camera/video source unavailable: {self.source}")
        return self

    def read(self):
        if self.capture is None:
            raise RuntimeError("Camera source has not been started")
        ok, frame = self.capture.read()
        if not ok and isinstance(self.source, str):
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ok, frame = self.capture.read()
        return ok, frame

    def release(self):
        if self.capture is not None:
            self.capture.release()
            self.capture = None
