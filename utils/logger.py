import logging
from datetime import datetime

def setup_logger():
    # Create logger
    logger = logging.getLogger('trading_bot')
    logger.setLevel(logging.INFO)
    
    # Create file handler
    log_filename = f"logs/trades.log"
    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.INFO)
    
    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger
