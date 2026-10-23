import logging

"""Utility logger setup for the project."""


def get_log(name: str) -> logging.Logger:
    """Return a configured logger instance for the given module name.

    The logger is set to INFO level and includes a console handler so log
    messages are printed consistently during application execution.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Use a consistent format for log output to make messages easier to read.
    log_format = logging.Formatter(fmt='%(name)s | %(levelname)s | %(message)s')

    # Attach a console handler so logs are emitted to the terminal.
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)

    # Avoid adding duplicate handlers when the same logger is reused.
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger
