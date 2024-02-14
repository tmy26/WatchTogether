import logging


def get_loggers(logger_name: str) -> object:
    """
    Retrieve the development logger with the specified name.
    :param logger_name: The name of the development logger.
    :type logger_name: string
    :rType: object
    :returns: The logger associated with the provided name.
    """
    return logging.getLogger(logger_name)
