import os
from queue import Queue
from video_analysis.streamer import Streamer
from video_analysis.detector import Detector
from video_analysis.displayer import Displayer
from video_analysis.video_metadata import VideoMetadataExtractor

VIDEO_FILE_NAME = "vid1.mp4"
OUTPUT_VIDEO_NAME = "output.mp4"  # Output file for the final processed video


def main() -> None:
    """Runs the video processing pipeline sequentially for easier debugging."""
    frame_queue: Queue = Queue()
    output_queue: Queue = Queue()

    video_path: str = os.path.join("videos", VIDEO_FILE_NAME)
    output_video_path: str = os.path.join("videos", OUTPUT_VIDEO_NAME)

    # Extract video metadata
    metadata_extractor = VideoMetadataExtractor(video_path)
    metadata = metadata_extractor.get_metadata()

    # Initialize components
    streamer: Streamer = Streamer(video_path, frame_queue)
    detector: Detector = Detector(frame_queue, output_queue)

    displayer: Displayer = Displayer(
        output_queue,
        output_video_path,
        frame_width=metadata["frame_width"],
        frame_height=metadata["frame_height"],
        fps=metadata["fps"],
    )

    # Run each component in sequence
    streamer.stream()  # Read and enqueue frames
    detector.detect()  # Process and enqueue detected frames
    displayer.display()  # Process and save final video


if __name__ == "__main__":
    main()
