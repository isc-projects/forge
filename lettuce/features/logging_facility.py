import logging
import sys

def logger_initialize(loglevel='INFO'):
    """
    Initialize logger instance common to the framework
    """
    # Get the instance of the common (named) logger
    logger = get_common_logger()
    logger_handler = logging.StreamHandler()
    # Parse the logging level specified as string (most likely from the config file)
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logger.setLevel(numeric_level)
    logger.addHandler(logger_handler)
    # This is the only message that is logged using the 'print' function because we
    # always want to have this message printed. Further log messages should go through
    # the logger.
    print('Logger has been successfully initialized to %s level' % loglevel.upper())
    return

def get_common_logger():
    """
    Returns instance of the common logger
    """
    return logging.getLogger('forge-main-logger')

