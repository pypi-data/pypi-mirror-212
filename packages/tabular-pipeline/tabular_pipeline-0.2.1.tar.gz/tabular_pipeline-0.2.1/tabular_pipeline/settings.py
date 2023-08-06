import logging
import os

from .util import create_dir

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")


BASE_OUTPUT_DIR = "output"
DEFAULT_STEP_FILE_NAME = "dataset.csv"
BASE_LOG_DIR = "logs"


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    create_dir(BASE_LOG_DIR)

    log_path = os.path.join(BASE_LOG_DIR, log_file)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


read_logger = setup_logger("read_logger", "read.log")
conform_logger = setup_logger("conform_logger", "conform.log")
normalise_logger = setup_logger("normalise_logger", "normalise.log")
