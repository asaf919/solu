import cv2


class VideoMetadataExtractor:
    """Extracts metadata from a video file such as width, height, and FPS."""

    def __init__(self, video_path: str) -> None:
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        # Extract metadata
        self.frame_width: int = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height: int = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps: int = int(
            self.cap.get(cv2.CAP_PROP_FPS) or 30
        )  # Default to 30 if undefined

        self.cap.release()  # Close video file

    def get_metadata(self) -> dict[str, int]:
        """Returns video metadata as a dictionary."""
        return {
            "frame_width": self.frame_width,
            "frame_height": self.frame_height,
            "fps": self.fps,
        }


if __name__ == "__main__":
    pass
