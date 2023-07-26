import logging


def get_loggers(dev_log_name: str):
    """
    This function returns the dev logger
    """
    return logging.getLogger(dev_log_name)
