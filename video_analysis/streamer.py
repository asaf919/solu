import cv2
from queue import Queue
from typing import Optional
from video_analysis.utils import get_logger, save_debug_output
from video_analysis.config import ENVIRONMENT, Environment


class Streamer:
    """Reads video frames and pushes them into a queue along with their timestamps."""

    def __init__(self, video_path: str, frame_queue: Queue) -> None:
        self.logger = get_logger("Streamer")
        self.video_path: str = video_path
        self.cap: cv2.VideoCapture = cv2.VideoCapture(video_path)
        self.frame_queue: Queue = frame_queue
        self.frame_count: int = 0

    def stream(self) -> None:
        """Reads video frames and sends them with timestamps to the queue."""
        self.logger.info("Starting streaming...")

        while self.cap.isOpened():
            ret: bool
            frame: Optional[cv2.Mat]
            ret, frame = self.cap.read()
            if not ret:
                break

            # Get the timestamp of the current frame
            timestamp: float = self.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

            # Push frame along with its timestamp
            self.frame_queue.put((frame, timestamp))
            self.frame_count += 1

            # Save frames only in DEBUG mode every 50 frames
            if ENVIRONMENT == Environment.DEBUG and self.frame_count % 50 == 0:
                save_debug_output(
                    "streamer",
                    f"frame_{self.frame_count}.jpg",
                    cv2.imencode(".jpg", frame)[1].tobytes(),
                )
                self.logger.info(
                    f"Saved debug frame {self.frame_count} at {timestamp:.2f} sec"
                )

        self.cap.release()
        self.frame_queue.put(None)  # End signal for the detector
        self.logger.info("Streaming complete.")


if __name__ == "__main__":
    pass
