import cv2
import numpy as np
from fastapi.testclient import TestClient
from app.main import app


def test_api_endpoints_and_demo_processing():
    with TestClient(app) as client:
        assert client.get("/api/health").status_code == 200
        frame = np.zeros((120, 160, 3), dtype=np.uint8)
        ok, encoded = cv2.imencode(".jpg", frame)
        assert ok
        response = client.post("/api/detection/process", content=encoded.tobytes())
        assert response.status_code == 200
        assert "detections" in response.json()
        assert client.get("/api/detections").status_code == 200
        assert client.get("/api/statistics").status_code == 200
        assert client.get("/api/statistics/performance").status_code == 200
        assert client.get("/api/alerts").status_code == 200
