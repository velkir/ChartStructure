import logging

def setup_logging():
    logging.basicConfig(filename='trends.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    logger_ccxt = logging.getLogger('ccxt')
    logger_ccxt.setLevel(logging.WARNING)

    logger_urllib3 = logging.getLogger('urllib3')
    logger_urllib3.setLevel(logging.WARNING)

    return logger

