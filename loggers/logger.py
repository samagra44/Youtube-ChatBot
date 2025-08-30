import logging
import os
from datetime import datetime

import sys
sys.dont_write_bytecode = True

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_filename = datetime.now().strftime("log_%Y-%m-%d_%H-%M-%S.log")
log_filepath = os.path.join(log_dir, log_filename)

logger = logging.getLogger("project_logger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler(log_filepath)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
