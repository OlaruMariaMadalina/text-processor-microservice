import logging
from app.config import LOG_LEVEL


logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
)


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger with the given name."""
    logger = logging.getLogger(name)
    return logger
