"""
Structured logging configuration for the application.
Provides consistent logging format with context information.
"""
import logging
import sys
from typing import Any
from datetime import datetime

from app.config import settings


# Custom log format with timestamp, level, module, and message
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class ContextFilter(logging.Filter):
    """
    Add contextual information to log records.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        # Add custom fields if they don't exist
        if not hasattr(record, 'request_id'):
            record.request_id = 'N/A'
        if not hasattr(record, 'user_id'):
            record.user_id = 'N/A'
        return True


def setup_logging() -> None:
    """
    Configure application-wide logging.
    Sets up console handler with appropriate format and level.
    """
    # Determine log level based on debug mode
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(formatter)
    
    # Add context filter
    console_handler.addFilter(ContextFilter())
    
    # Add handler to root logger
    root_logger.addHandler(console_handler)
    
    # Set specific log levels for third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.DEBUG else logging.WARNING
    )
    logging.getLogger("celery").setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Module name (typically __name__)
    
    Returns:
        Logger instance configured with application settings
    
    Example:
        logger = get_logger(__name__)
        logger.info("Processing request", extra={"request_id": "123"})
    """
    return logging.getLogger(name)


# Initialize logging on module import
setup_logging()
