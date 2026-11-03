import logging
import os

BASIC_CONFIG = {"level": logging.DEBUG,
                # "filename": os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.log"),
                "format": "[%(asctime)s %(levelname)-7s ] %(name)s: %(message)s",
                "datefmt": "%H:%M:%S", }
class Logger():
    class UncorrectLogLevelError(Exception): pass
    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.supports_levels = [
            "debug",
            "info",
            "warn",
            "critical",
            "error",
        ]
        self.config = {"level": logging.DEBUG,
                "format": "%(asctime)s %(levelname)-7s %(name)s: %(message)s",
                "datefmt": "%H:%M:%S", }
        self.logging.basicConfig(self.config)
    def setLevel(self, level):
        if not level in self.supports_levels:
            raise self.UncorrectLogLevelError(f"Uncorrect log level {level}")
    def debug(self): pass