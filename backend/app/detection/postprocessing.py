def filter_by_confidence(detections: list[dict], threshold: float) -> list[dict]:
    return [d for d in detections if float(d["confidence"]) >= threshold]
