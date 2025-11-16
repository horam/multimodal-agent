import logging
from logging import handlers
import sys as system

def get_logger(name: str = "multimodal_agent")-> logging.Logger:
    """
    Create or retrieve a module-level logger with a sane configuration.
    This avoids duplicate handlers and ensures consistent format.
    """
    
    logger = logging.getLogger(name)
    
    if not logger:
        logger.setLevel(logging.info)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        handlers.setFormatter(formatter)
        
        logger.propagate = False
        
    
    return logger