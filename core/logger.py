import sys

from loguru import logger


# Инициализация логгера
def init_logger() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="DEBUG",
        colorize=True
    )
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="1 week",
        compression="zip"
    )
    logger.add(
        "logs/error.log",
        level="ERROR",
        rotation="1 week",
        retention="1 month",
        compression="zip"
    )
