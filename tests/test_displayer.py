import pytest
from queue import Queue
from video_analysis.displayer import Displayer


@pytest.fixture
def output_queue() -> Queue:
    """Creates a test output queue."""
    return Queue()


def test_displayer_does_not_crash(output_queue: Queue) -> None:
    """Ensure Displayer starts and stops correctly."""
    displayer = Displayer(output_queue)

    output_queue.put(None)  # Signal to exit immediately
    displayer.display()

    assert output_queue.empty()  # Ensure queue is consumed
