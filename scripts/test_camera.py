import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
from app.detection.camera import CameraSource

source = CameraSource(0).start()
ok, frame = source.read()
source.release()
print(f"Camera read: {ok}; frame shape: {None if frame is None else frame.shape}")
