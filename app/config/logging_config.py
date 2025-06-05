import logging

from loguru import logger


logger_1 = logging.getLogger()
logger_1.handlers.clear()
logger_1.setLevel(logging.INFO)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    # Перехват логгеров
    logging.getLogger("uvicorn").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    logging.getLogger("fastapi").handlers = [InterceptHandler()]
    logger_1.handlers = [InterceptHandler()]


# Логгирование в файл

# logger.add(
#     'app.log',
#     level='INFO',
#     format='{time} - {level} - {message}',
#     rotation='10 KB',
#     compression="zip"
# )
