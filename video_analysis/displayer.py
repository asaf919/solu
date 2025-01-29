import cv2
from queue import Queue
from video_analysis.utils import get_logger
from video_analysis.detector_result import DetectionResult


class Displayer:
    """Processes and saves detected frames into a video file."""

    def __init__(
        self,
        output_queue: Queue,
        output_video_path: str,
        frame_width: int,
        frame_height: int,
        fps: int = 30,
    ) -> None:
        self.logger = get_logger("Displayer")
        self.output_queue: Queue = output_queue
        self.output_video_path: str = output_video_path
        self.frame_width: int = frame_width
        self.frame_height: int = frame_height
        self.fps: int = fps

        # Initialize the video writer
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for MP4
        self.video_writer = cv2.VideoWriter(
            self.output_video_path,
            fourcc,
            self.fps,
            (self.frame_width, self.frame_height),
        )

    def process_frame(self, detection_result: DetectionResult) -> cv2.Mat:
        """Draws detections and timestamp on the frame."""
        frame = detection_result.frame.copy()

        # Draw bounding boxes for detections
        for detection in detection_result.detections:
            x, y, w, h = detection["x"], detection["y"], detection["w"], detection["h"]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green boxes

        # Overlay timestamp on frame
        timestamp_text = f"Time: {detection_result.timestamp:.2f} sec"
        cv2.putText(
            frame,
            timestamp_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        return frame

    def display(self) -> None:
        """Reads processed frames, overlays detections, and writes them to video."""
        self.logger.info("Starting video processing...")

        while True:
            detection_result: DetectionResult | None = self.output_queue.get()
            if detection_result is None:
                break  # Stop processing if no more frames

            processed_frame = self.process_frame(detection_result)
            self.video_writer.write(processed_frame)  # Save to video

        self.video_writer.release()  # Finalize video file
        self.logger.info(f"Video saved at {self.output_video_path}")


if __name__ == "__main__":
    pass
