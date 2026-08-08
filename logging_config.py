import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    # Create a logger
    logger = logging.getLogger("vanilla_rag_logger")

    # Avoid adding multiple handlers if the logger already has handlers
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)  # Set the logger to capture INFO and higher levels

        # Define the log format and date format
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        date_format = '%d-%m-%Y %H:%M:%S'

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Only INFO and above will be captured
        console_format = logging.Formatter(fmt=log_format, datefmt=date_format)
        console_handler.setFormatter(console_format)

        # File handler with rotating logs
        rotating_handler = RotatingFileHandler("vanilla_rag.log", maxBytes=5 * 1024 * 1024, backupCount=3) # 5MB
        rotating_handler.setLevel(logging.INFO)  # INFO and above will be captured
        file_format = logging.Formatter(fmt=log_format, datefmt=date_format)
        rotating_handler.setFormatter(file_format)

        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(rotating_handler)
        logger.propagate = False  # Disable propagation

    return logger