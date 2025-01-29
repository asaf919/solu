# import pytest
# import cv2
# from queue import Queue
# from video_analysis.detector import Detector
#
#
# @pytest.fixture
# def test_frame() -> cv2.Mat:
#     """Generate a blank test frame."""
#     return cv2.imread("test_face.jpg")  # Use a test image with a face
#
#
# @pytest.fixture
# def frame_queues() -> tuple[Queue, Queue]:
#     """Creates a test frame queue and output queue."""
#     return Queue(), Queue()
#
#
# def test_detector_detect_faces(
#     test_frame: cv2.Mat, frame_queues: tuple[Queue, Queue]
# ) -> None:
#     """Ensure Detector detects at least one face in a known image."""
#     frame_queue, output_queue = frame_queues
#     detector = Detector(frame_queue, output_queue)
#
#     frame_queue.put(test_frame)
#     frame_queue.put(None)  # End signal
#
#     detector.detect()
#
#     processed_frame = output_queue.get()
#     assert processed_frame is not None  # The frame should be returned
