import logging
from app.gps.gps_provider import GPSProvider
from app.gps.mock_gps import MockGPS

logger = logging.getLogger(__name__)


class SerialGPS(GPSProvider):
    """Future hardware adapter; safely falls back until a serial NMEA receiver is configured."""
    def __init__(self, fallback: GPSProvider | None = None):
        self.fallback = fallback or MockGPS()

    def get_location(self) -> dict[str, float]:
        logger.warning("Serial GPS is not configured; using mock/last-known fallback")
        return self.fallback.get_location()
