import os
import shutil
from enum import Enum


class Environment(Enum):
    DEBUG = "debug"
    PRODUCTION = "production"


# Set environment mode
ENVIRONMENT = (
    Environment.DEBUG
)  # Change to Environment.PRODUCTION when running in production

# Define debug output folder
BASE_OUTPUT_FOLDER = os.path.join(os.getcwd(), "debug_output")

# If in DEBUG mode, ensure fresh debug folder
if ENVIRONMENT == Environment.DEBUG:
    if os.path.exists(BASE_OUTPUT_FOLDER):
        shutil.rmtree(BASE_OUTPUT_FOLDER)  # Delete old debug files
    os.makedirs(BASE_OUTPUT_FOLDER)
    os.makedirs(os.path.join(BASE_OUTPUT_FOLDER, "streamer"))
    os.makedirs(os.path.join(BASE_OUTPUT_FOLDER, "detector"))
    os.makedirs(os.path.join(BASE_OUTPUT_FOLDER, "displayer"))
