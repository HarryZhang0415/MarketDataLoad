import logging
import os

class LoggingService:
    def __init__(self, name, level=logging.INFO, log_file=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.parent = logging.getLogger()

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self._formatter = formatter
        self._log_path = log_file
        self._level = level

        # Add console handler
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # Add file handler
        if log_file is not None:
            fh = logging.FileHandler(log_file)
            fh.setLevel(level)
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    @property
    def formatter(self):
        return self._formatter
    
    @property
    def log_path(self):
        return self._log_path
    
    @property
    def level(self):
        return self._level

    def addHandler(self, handler):
        self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)