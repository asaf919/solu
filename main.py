import os
import threading
from queue import Queue
from video_analysis.streamer import Streamer
from video_analysis.detector import Detector
from video_analysis.displayer import Displayer
from video_analysis.video_metadata import VideoMetadataExtractor

VIDEO_FILE_NAME = "vid1.mp4"
OUTPUT_VIDEO_NAME = "output.mp4"  # Output file for the final processed video


def main() -> None:
    """Runs the video processing pipeline in parallel using multithreading."""
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

    # Create and start threads
    stream_thread = threading.Thread(target=streamer.stream, name="Streamer-Thread")
    detect_thread = threading.Thread(target=detector.detect, name="Detector-Thread")
    display_thread = threading.Thread(target=displayer.display, name="Displayer-Thread")

    stream_thread.start()
    detect_thread.start()
    display_thread.start()

    # Wait for streamer to finish, then signal detector
    stream_thread.join()
    frame_queue.put(None)  # Ensure detector knows streamer is done

    # Wait for detector to finish, then signal displayer
    detect_thread.join()
    output_queue.put(None)  # Ensure displayer knows detector is done

    # Wait for displayer to finish
    display_thread.join()


if __name__ == "__main__":
    main()
