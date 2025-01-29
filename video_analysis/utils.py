import logging
import os
from video_analysis.config import ENVIRONMENT, Environment, BASE_OUTPUT_FOLDER


def get_logger(logger_name: str):
    """Configures a logger that always logs to a file and console."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Create handlers
    console_handler = logging.StreamHandler()
    log_file = (
        os.path.join(BASE_OUTPUT_FOLDER, f"{logger_name}.log")
        if ENVIRONMENT == Environment.DEBUG
        else f"{logger_name}.log"
    )
    file_handler = logging.FileHandler(log_file, mode="w")

    # Log format with thread names for debugging
    log_format = "%(asctime)s - [%(threadName)s] - %(name)s - %(levelname)s - %(message)s  [%(filename)s, function: %(funcName)s, line: %(lineno)d]"
    formatter = logging.Formatter(log_format)

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def save_debug_output(component_name: str, filename: str, data) -> None:
    """Save debug outputs like images or text files if in DEBUG mode."""
    if ENVIRONMENT == Environment.DEBUG:
        output_path = os.path.join(BASE_OUTPUT_FOLDER, component_name, filename)
        with open(output_path, "wb") as f:
            f.write(data)


if __name__ == "__main__":
    pass
