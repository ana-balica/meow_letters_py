import logging
import logging.config


def getLogger(name):
    """ Override logging.getLogger() to load the log config.
    If you want to change logging configuration, make changes to the config file 
    from configs folder.

    Usage in other files::

        from meow_letters import log
        logging = log.getLogger(__name__)

    :param name: filename origin of logging
    :return: logger object
    """
    logging.config.fileConfig('configs/logging.conf')
    logger = logging.getLogger(name)
    return logger


if __name__ == '__main__':
    logging = getLogger(__name__)
    logging.debug("Debug info")
    logging.info("Info here")
    logging.warning("Warning info")
    logging.error("Error here")
