# import pytest
# import os
# import cv2
# from queue import Queue
# from video_analysis.streamer import Streamer
#
#
# VIDEO_PATH = "videos/vid1.mp4"
#
#
# def test_print_working_directory():
#     """Prints the working directory to debug path issues."""
#     print(f"\nCurrent Working Directory: {os.getcwd()}")  # Debugging output
#     assert os.path.exists(VIDEO_PATH), f"Test video file '{VIDEO_PATH}' not found."
#

# def test_streamer_initialization():
#     """Tests if Streamer initializes correctly."""
#     frame_queue = Queue()
#     streamer = Streamer(VIDEO_PATH, frame_queue)
#
#     assert streamer.video_path == VIDEO_PATH
#     assert isinstance(streamer.cap, cv2.VideoCapture)
#
#
#
# def test_streamer_reads_frames():
#     """Tests if Streamer reads at least one frame."""
#     frame_queue = Queue()
#     streamer = Streamer("videos/vid1.mp4", frame_queue)
#
#     streamer.stream()
#     assert not frame_queue.empty()  # Should contain frames
