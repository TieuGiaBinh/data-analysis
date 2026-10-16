import logging


def get_log(msg: str) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    log_format = logging.Formatter(fmt='%(name)s | %(levelname)s | %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    return logger
