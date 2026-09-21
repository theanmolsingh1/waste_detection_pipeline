import numpy as np
from app.detection.preprocessing import FramePreprocessor
from app.detection.postprocessing import filter_by_confidence
from app.gps.mock_gps import MockGPS

def test_preview_dimensions():
    value = FramePreprocessor().prepare_preview(np.zeros((480, 640, 3), dtype=np.uint8))
    assert value.shape == (224, 224, 3)
    assert value.dtype == np.float32

def test_confidence_filter():
    values = [{"confidence": .8}, {"confidence": .4}]
    assert filter_by_confidence(values, .6) == [{"confidence": .8}]

def test_mock_gps_coordinates():
    location = MockGPS().get_location()
    assert -90 <= location["latitude"] <= 90
    assert -180 <= location["longitude"] <= 180
