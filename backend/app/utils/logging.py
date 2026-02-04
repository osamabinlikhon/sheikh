import logging
from loguru import logger
from app.config import settings

class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())

def setup_logging():
    logging.getLogger("uvicorn").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    logger.add(
        "file_{time}.log",
        rotation="1 day",
        level=settings.log_level,
        serialize=False
    )
