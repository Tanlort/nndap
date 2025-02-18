import logging

def setup_logger(log_filename: str) -> logging.Logger:
    
    logger = logging.getLogger(log_filename)
    if not logger.hasHandlers():  # Prevent duplicate handlers
        handler = logging.FileHandler(log_filename)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
