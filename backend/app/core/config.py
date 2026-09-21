from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./waste_detection.db"
    confidence_threshold: float = 0.60
    gps_mode: str = "mock"
    camera_source: str = "0"
    model_path: str = "models/waste_model.pt"
    demo_mode: bool = True
    alert_cooldown_seconds: int = 30
    mock_latitude: float = 12.9716
    mock_longitude: float = 77.5946
    detection_image_dir: str = "detections"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def camera_value(self):
        return int(self.camera_source) if self.camera_source.isdigit() else self.camera_source

    @property
    def model_file(self) -> Path:
        return Path(self.model_path)


@lru_cache
def get_settings() -> Settings:
    return Settings()
