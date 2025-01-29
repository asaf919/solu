import cv2
from queue import Queue
from video_analysis.utils import get_logger
from video_analysis.detector_result import DetectionResult


class Displayer:
    """Processes and saves detected frames into a video file with blurred detections."""

    def __init__(
        self,
        output_queue: Queue,
        output_video_path: str,
        frame_width: int,
        frame_height: int,
        fps: int = 30,
        memory_decay: int = 8,  # Number of frames to keep blurring after motion stops
        blur_strength: tuple[int, int] = (17, 17),  # Kernel size for Gaussian blur
        padding: int = 12,  # Extra padding to ensure full object coverage
        log_every_n: int = 50,  # Log progress every N frames
    ) -> None:
        self.logger = get_logger("Displayer")
        self.output_queue: Queue = output_queue
        self.output_video_path: str = output_video_path
        self.frame_width: int = frame_width
        self.frame_height: int = frame_height
        self.fps: int = fps
        self.memory_decay: int = memory_decay
        self.blur_strength: tuple[int, int] = blur_strength
        self.padding: int = padding
        self.log_every_n: int = log_every_n
        self.frame_count: int = 0  # Track processed frames

        # Memory buffer for keeping blur active on recent detections
        self.blur_memory: list[list[dict[str, int]]] = []

        # Initialize the video writer
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for MP4
        self.video_writer = cv2.VideoWriter(
            self.output_video_path,
            fourcc,
            self.fps,
            (self.frame_width, self.frame_height),
        )

    def process_frame(self, detection_result: DetectionResult) -> cv2.Mat:
        """Blurs detections with memory retention and overlays timestamp."""
        frame = detection_result.frame.copy()
        self.frame_count += 1  # Track processed frames

        # Store detections in memory to prevent instant blur disappearance
        self.blur_memory.append(detection_result.detections)
        if len(self.blur_memory) > self.memory_decay:
            self.blur_memory.pop(0)  # Keep only recent detections

        # Apply blurring for both current and past detections
        for past_detections in self.blur_memory:
            for detection in past_detections:
                # Expand the bounding box slightly for better coverage
                x = max(detection["x"] - self.padding, 0)
                y = max(detection["y"] - self.padding, 0)
                w = min(detection["w"] + 2 * self.padding, self.frame_width - x)
                h = min(detection["h"] + 2 * self.padding, self.frame_height - y)

                # Extract the region of interest (ROI)
                roi = frame[y : y + h, x : x + w]

                # Apply Gaussian blur
                blurred_roi = cv2.GaussianBlur(roi, self.blur_strength, 0)

                # Replace original ROI with the blurred one
                frame[y : y + h, x : x + w] = blurred_roi

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

        # Log progress every `log_every_n` frames
        if self.frame_count % self.log_every_n == 0:
            self.logger.info(
                f"Processed frame {self.frame_count} at {detection_result.timestamp:.2f} sec - {len(detection_result.detections)} regions blurred"
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
