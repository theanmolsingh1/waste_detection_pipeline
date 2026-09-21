from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class AlertProvider(ABC):
    @abstractmethod
    def send(self, detection: dict) -> bool: ...


class ConsoleAlert(AlertProvider):
    def send(self, detection: dict) -> bool:
        logger.info("ALERT | %s | %.0f%% | %.4f, %.4f | %s", detection["waste_type"], detection["confidence"] * 100, detection["latitude"], detection["longitude"], detection["timestamp"])
        return True


class DashboardAlert(AlertProvider):
    """Persistence makes alerts visible through the dashboard API."""
    def send(self, detection: dict) -> bool:
        return True
