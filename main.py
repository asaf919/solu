import os
import threading
from queue import Queue
from video_analysis.streamer import Streamer
from video_analysis.detector import Detector
from video_analysis.displayer import Displayer

VIDEO_FILE_NAME = "vid1.mp4"


def main() -> None:
    """Sets up and starts the video processing pipeline."""
    frame_queue: Queue = Queue()
    output_queue: Queue = Queue()

    video_path: str = os.path.join("videos", VIDEO_FILE_NAME)

    # Initialize components
    streamer: Streamer = Streamer(video_path, frame_queue)
    detector: Detector = Detector(frame_queue, output_queue)
    displayer: Displayer = Displayer(output_queue)

    # Start threads for each component
    stream_thread: threading.Thread = threading.Thread(
        target=streamer.stream, name="Streamer-Thread"
    )
    detect_thread: threading.Thread = threading.Thread(
        target=detector.detect, name="Detector-Thread"
    )
    display_thread: threading.Thread = threading.Thread(
        target=displayer.display, name="Displayer-Thread"
    )

    stream_thread.start()
    detect_thread.start()
    display_thread.start()

    # Ensure all threads complete execution
    stream_thread.join()
    frame_queue.put(None)  # Ensure detector knows streamer is done

    detect_thread.join()
    output_queue.put(None)  # Ensure displayer knows detector is done

    display_thread.join()


if __name__ == "__main__":
    main()
