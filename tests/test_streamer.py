import pytest
import cv2
from queue import Queue
from video_analysis.streamer import Streamer


@pytest.fixture
def frame_queue() -> Queue:
    """Creates a test frame queue."""
    return Queue()


def test_streamer_initialization(frame_queue: Queue) -> None:
    """Ensure the Streamer initializes correctly."""
    streamer = Streamer("videos/vid1.mp4", frame_queue)
    assert streamer.video_path == "videos/vid1.mp4"


def test_streamer_stream(mocker, frame_queue: Queue) -> None:
    """Check if Streamer reads at least one frame."""
    mocker.patch.object(cv2, "VideoCapture", autospec=True)  # Mock video capture
    streamer = Streamer("videos/vid1.mp4", frame_queue)
    streamer.stream()

    assert not frame_queue.empty()  # Frames should be added
    frame = frame_queue.get()
    assert frame is not None  # A valid frame should be received
