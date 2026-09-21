from abc import ABC, abstractmethod


class GPSProvider(ABC):
    @abstractmethod
    def get_location(self) -> dict[str, float]:
        """Return latitude/longitude without raising for normal device failures."""
