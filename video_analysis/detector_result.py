import numpy as np
from typing import Any


class DetectionResult:
    """Encapsulates motion detection results."""

    def __init__(
        self, frame: np.ndarray, timestamp: float, detections: list[dict[str, Any]]
    ) -> None:
        self.frame = frame
        self.timestamp = timestamp
        self.detections = detections

    def to_dict(self) -> dict[str, Any]:
        """Convert the detection result to a dictionary."""
        return {"timestamp": self.timestamp, "detections": self.detections}


if __name__ == "__main__":
    pass
