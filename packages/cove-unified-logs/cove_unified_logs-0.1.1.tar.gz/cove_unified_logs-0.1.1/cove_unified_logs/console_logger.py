import logging


class ConsoleLogger:
    def __init__(self):
        pass

    def _put_log_event(self, level, message, **metadata):
        # Put the log event to the console
        logging.getLogger().log(level, message, extra=metadata)

    def debug(self, message, **metadata):
        self._put_log_event(logging.DEBUG, message, **metadata)

    def info(self, message, **metadata):
        self._put_log_event(logging.INFO, message, **metadata)

    def warning(self, message, **metadata):
        self._put_log_event(logging.WARNING, message, **metadata)

    def error(self, message, **metadata):
        self._put_log_event(logging.ERROR, message, **metadata)

    def critical(self, message, **metadata):
        self._put_log_event(logging.CRITICAL, message, **metadata)

