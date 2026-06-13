# Shinobu Music Bot
# Owner: @Sanji_fr

import os
import sys
from os import listdir, mkdir

from ..logging import LOGGER


def dirr():
    if "assets" not in listdir():
        LOGGER(__name__).error(
            "Assets folder not found. Please make sure you cloned the full repository."
        )
        sys.exit()

    # Clean up stale image files from previous sessions
    for file in os.listdir():
        if file.endswith((".jpg", ".jpeg", ".png")):
            os.remove(file)

    # Ensure required directories exist
    for folder in ("downloads", "cache"):
        if folder not in listdir():
            mkdir(folder)

    LOGGER(__name__).info("Directories verified and cleaned.")