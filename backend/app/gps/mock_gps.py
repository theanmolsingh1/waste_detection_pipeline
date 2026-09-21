from app.core.config import get_settings
from app.gps.gps_provider import GPSProvider


class MockGPS(GPSProvider):
    def get_location(self) -> dict[str, float]:
        s = get_settings()
        return {"latitude": s.mock_latitude, "longitude": s.mock_longitude}
