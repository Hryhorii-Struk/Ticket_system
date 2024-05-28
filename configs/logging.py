import logging


class LoggingConfig:
    LOG_FILE = 'ticket_system.log'
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'


def DEBUG():
    return None