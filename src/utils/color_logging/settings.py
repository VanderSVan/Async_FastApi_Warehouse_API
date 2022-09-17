import logging
import logging.config
from pathlib import Path

ESCAPE_SEQUENCE = {
    'HEXADECIMAL': "\x1b[",
    'UNICODE': "\u001b",
    'OCTAL': "\033["
}

STYLE = {
    'NORMAL': "0",
    'BOLD': "1",
    'LIGHT': "2",
    'ITALICIZED': "3",
    'UNDERLINED': "4",
    'BLINK': "5"
}

TEXT_COLOR = {
    'BLACK': "30",
    'RED': "31",
    'GREEN': "32",
    'YELLOW': "33",
    'BLUE': "34",
    'PURPLE': "35",
    'CYAN': "36",
    'WHITE': "37"
}

BACKGROUND_COLOR = {
    'BLACK': "40",
    'RED': "41",
    'GREEN': "42",
    'YELLOW': "43",
    'BLUE': "44",
    'PURPLE': "45",
    'CYAN': "46",
    'WHITE': "47"
}

# create 'logs' folder
current_folder = Path(__file__).parent.absolute()
log_folder = current_folder.joinpath('logs')
log_folder.mkdir(parents=True, exist_ok=True)


def get_colored_string(text: str,
                       esc_seq: str = ESCAPE_SEQUENCE['OCTAL'],
                       style: str = None,
                       text_color: str = None,
                       background_color: str = None) -> str:
    """
    Makes a color string by parameters.
    :return: "<esc_seq><style><separator><text_color><separator><background_color><stopper><reset_color>"
    """
    separator = ';'
    stopper = 'm'
    reset_color = [esc_seq, '0m']
    colored_string: list = [
        esc_seq,
        style if style else "0",
        separator + text_color if text_color else "",
        separator + background_color if background_color else "",
        stopper,
        text,
        *reset_color
    ]
    return ''.join(colored_string)


def get_colored_string_by_log_level_name(level_name: str, message: str):
    level_name = level_name.upper()

    match level_name:
        case 'DEBUG':
            return get_colored_string(text=message,
                                      style=STYLE['BOLD'])
        case 'SUCCESS':
            return get_colored_string(text=message,
                                      style=STYLE['BOLD'],
                                      text_color=TEXT_COLOR['GREEN'])
        case 'INFO':
            return get_colored_string(text=message,
                                      style=STYLE['BOLD'],
                                      text_color=TEXT_COLOR['BLUE'])
        case 'WARNING':
            return get_colored_string(text=message,
                                      style=STYLE['BOLD'],
                                      text_color=TEXT_COLOR['YELLOW'])
        case 'ERROR':
            return get_colored_string(text=message,
                                      style=STYLE['BOLD'],
                                      text_color=TEXT_COLOR['RED'])
        case 'CRITICAL':
            return get_colored_string(text=message,
                                      style=STYLE['BOLD'],
                                      text_color=TEXT_COLOR['BLACK'],
                                      background_color=BACKGROUND_COLOR['RED'])
        case _:
            return get_colored_string(text=message)


def add_log_level(level_name, level_number, method_name=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.
    `level_name` becomes an attribute of the `logging` module with the value
    `level_number`. `method_name` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `method_name` is not specified, `level_name.lower()` is
    used.
    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present
    Example
    -------
    >>> add_log_level('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5
    """
    if not method_name:
        method_name = level_name.lower()

    if hasattr(logging, level_name):
        raise AttributeError(f'{level_name} already defined in logging module')
    if hasattr(logging, method_name):
        raise AttributeError(f'{method_name} already defined in logging module')
    if hasattr(logging.getLoggerClass(), method_name):
        raise AttributeError(f'{method_name} already defined in color_logger class')

    def log_for_level(self, message, *args, **kwargs):
        if self.isEnabledFor(level_number):
            self._log(level_number, message, args, **kwargs)

    def log_to_root(message, *args, **kwargs):
        logging.log(level_number, message, *args, **kwargs)

    logging.addLevelName(level_number, level_name)
    setattr(logging, level_name, level_number)
    setattr(logging.getLoggerClass(), method_name, log_for_level)
    setattr(logging, method_name, log_to_root)


class ColoredFormatter(logging.Formatter):
    def __init__(self, *, format):
        logging.Formatter.__init__(self, fmt=format)

    def format(self, record):
        msg = super().format(record)
        level_name = record.levelname
        if level_name:
            result = get_colored_string_by_log_level_name(level_name, msg)
        else:
            result = msg
        return result


# Add new logging level
add_log_level('SUCCESS', logging.DEBUG + 5)

logger_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)s - %(message)s"
        },
        'color': {
            'format': "%(levelname)s - %(module)s:%(funcName)s:%(lineno)s - %(message)s",
            '()': ColoredFormatter
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'color',
            'stream': 'ext://sys.stdout'
        },
        'debug_file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': log_folder.joinpath('debug.log'),
            'when': 'midnight',
            'backupCount': 20,
            'encoding': 'utf8'
        },
        'info_file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'filename': log_folder.joinpath('info.log'),
            'when': 'midnight',
            'backupCount': 20,
            'encoding': 'utf8'
        },
        'warning_file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'WARNING',
            'formatter': 'standard',
            'filename': log_folder.joinpath('warning.log'),
            'when': 'midnight',
            'backupCount': 20,
            'encoding': 'utf8'
        },
        'error_file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'standard',
            'filename': log_folder.joinpath('error.log'),
            'when': 'midnight',
            'backupCount': 20,
            'encoding': 'utf8'
        },
        'critical_file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'CRITICAL',
            'formatter': 'standard',
            'filename': log_folder.joinpath('critical.log'),
            'when': 'midnight',
            'backupCount': 20,
            'encoding': 'utf8'
        }

    },
    'loggers': {
        'console': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False
        },
        'files': {
            'level': 'DEBUG',
            'handlers': ['debug_file_handler', 'info_file_handler',
                         'warning_file_handler', 'error_file_handler',
                         'critical_file_handler'],
            'propagate': False
        },
        'full': {
            'level': 'DEBUG',
            'handlers': ['console', 'debug_file_handler',
                         'info_file_handler', 'warning_file_handler',
                         'error_file_handler', 'critical_file_handler'],
            'propagate': False
        }
    }
}
