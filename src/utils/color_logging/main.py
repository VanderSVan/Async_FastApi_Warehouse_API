import logging.config
from typing import NoReturn

from src.utils.color_logging.settings import logger_config


def set_level_for_other_loggers(excluding: list, level_name: str = 'CRITICAL') -> NoReturn:
    level_names: tuple = ('DEBUG', 'SUCCESS', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')

    if level_name.upper() in level_names:
        processed_level_name = level_name.upper()
    else:
        processed_level_name = 'ERROR'

    for logger_name in logging.Logger.manager.loggerDict:
        if logger_name.split('.')[0] in excluding:
            continue
        else:
            logging.getLogger(logger_name).setLevel(processed_level_name)


set_level_for_other_loggers(excluding=['uvicorn', 'sqlalchemy', 'celery'], level_name='ERROR')
logging.config.dictConfig(logger_config)
logger = logging.getLogger('full')


if __name__ == '__main__':
    logger.debug(f"Debug message with level number is {logging.DEBUG}")
    logger.success(f"Success message with level number is {logging.SUCCESS}")
    logger.info(f"Info message with level number is {logging.INFO}")
    logger.warning(f"Warning message with level number is {logging.WARNING}")
    logger.error(f"Error message with level number is {logging.ERROR}")
    logger.exception(f"Exception message with level number is {logging.ERROR}")
    logger.critical(f"Critical message with level number is {logging.CRITICAL}")
