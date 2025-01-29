import os
import argparse
from queue import Queue
from video_analysis.streamer import Streamer
from video_analysis.detector import Detector
from video_analysis.displayer import Displayer
from video_analysis.video_metadata import VideoMetadataExtractor


OUTPUT_VIDEO_NAME = "output.mp4"


def main(input_video: str) -> None:
    """Runs the video processing pipeline sequentially for easier debugging."""
    frame_queue: Queue = Queue()
    output_queue: Queue = Queue()

    video_path: str = os.path.join("videos", input_video)

    # Extract video metadata
    metadata_extractor = VideoMetadataExtractor(video_path)
    metadata = metadata_extractor.get_metadata()

    # Initialize components
    streamer: Streamer = Streamer(video_path, frame_queue)
    detector: Detector = Detector(frame_queue, output_queue)

    displayer: Displayer = Displayer(
        output_queue,
        OUTPUT_VIDEO_NAME,
        frame_width=metadata["frame_width"],
        frame_height=metadata["frame_height"],
        fps=metadata["fps"],
    )

    # Run each component in sequence
    streamer.stream()  # Read and enqueue frames
    detector.detect()  # Process and enqueue detected frames
    displayer.display()  # Process and save final video


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run video motion detection sequential pipeline.")
    parser.add_argument(
        "--input_video", type=str, required=True, help="Path to the input video file."
    )
    args = parser.parse_args()

    main(args.input_video)
