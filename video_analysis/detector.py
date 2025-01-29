import cv2
import numpy as np
from queue import Queue
from video_analysis.utils import get_logger
from video_analysis.detector_result import DetectionResult


class Detector:
    """Detects motion in video frames and stores results."""

    def __init__(
        self, frame_queue: Queue, output_queue: Queue, log_every_n: int = 50
    ) -> None:
        self.logger = get_logger("Detector")
        self.frame_queue: Queue = frame_queue
        self.output_queue: Queue = output_queue
        self.background_model: np.ndarray | None = None  # Background accumulator
        self.frame_count: int = 0  # Track processed frames
        self.log_every_n: int = log_every_n  # Log frequency

    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """Converts frame to grayscale and applies Gaussian blur."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.GaussianBlur(gray, (21, 21), 0)

    def update_background(self, gray: np.ndarray) -> None:
        """Updates the background model."""
        if self.background_model is None:
            self.background_model = np.float32(gray)
        else:
            cv2.accumulateWeighted(gray, self.background_model, 0.05)

    def get_motion_detections(self, gray: np.ndarray) -> list[dict]:
        """Finds motion regions by computing differences with the background model."""
        background = cv2.convertScaleAbs(self.background_model)
        frame_delta = cv2.absdiff(background, gray)

        # Apply thresholding
        _, thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, None, iterations=2)  # Fill gaps

        return self.extract_contours(thresh)

    def extract_contours(self, thresh: np.ndarray) -> list[dict]:
        """Extracts bounding boxes of motion from thresholded image."""
        contours, _ = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        detections = []
        for contour in contours:
            if cv2.contourArea(contour) < 500:  # Ignore small noise
                continue

            x, y, w, h = cv2.boundingRect(contour)
            detections.append({"x": x, "y": y, "w": w, "h": h})

        return detections

    def detect(self) -> None:
        """Detects motion by comparing frames to an adaptive background model."""
        self.logger.info("Starting detection...")

        while True:
            data: tuple[np.ndarray, float] | None = self.frame_queue.get()
            if data is None:
                self.output_queue.put(None)  # Signal end of processing
                break

            frame, timestamp = data  # Unpack frame and timestamp
            gray = self.preprocess_frame(frame)
            self.frame_count += 1  # Track processed frames

            # Handle first frame: Initialize background, skip motion detection
            if self.background_model is None:
                self.background_model = np.float32(gray)
                self.logger.info(f"Initialized background model at {timestamp:.2f} sec")
                continue  # Skip processing the first frame

            detections = self.get_motion_detections(gray)
            detection_result = DetectionResult(frame, timestamp, detections)
            self.output_queue.put(detection_result)

            self.update_background(gray)

            # Log progress every `log_every_n` frames
            if self.frame_count % self.log_every_n == 0:
                self.logger.info(
                    f"Processing frame {self.frame_count} at {timestamp:.2f} sec - {len(detections)} motions detected in this frame."
                )

        self.logger.info("Detection complete.")


if __name__ == "__main__":
    pass
