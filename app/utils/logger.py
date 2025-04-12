import logging
import sys

try:
    from colorlog import ColoredFormatter
    use_colors = True
except ImportError:
    use_colors = False

def get_logger(name: str, level=logging.DEBUG, log_to_file: str = None) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger  # Avoid duplicate handlers

    logger.setLevel(level)

    stream_handler = logging.StreamHandler(sys.stdout)
    if use_colors:
        formatter = ColoredFormatter(
            "%(log_color)s[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            datefmt='%H:%M:%S',
            log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'bold_red',
            }
        )
    else:
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s", datefmt='%H:%M:%S')

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_to_file:
        file_handler = logging.FileHandler(log_to_file)
        file_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(file_handler)

    return logger
