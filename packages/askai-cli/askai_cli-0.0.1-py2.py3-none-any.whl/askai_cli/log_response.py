import logging
from logging.handlers import TimedRotatingFileHandler


class LogResponse:

    def __init__(self, path):
        self.logger = logging.getLogger("askai log")
        self.path = path

    def create_rotating_chat_logger(self):
        self.logger.setLevel(logging.INFO)
        handler = TimedRotatingFileHandler(self.path+"/askai.log", when="d")
        self.logger.addHandler(handler)
        return self.logger

    def print_and_log(self, input_str):
        print(input_str)
        self.logger.info(input_str)

    def log(self, input_str):
        self.logger.info(input_str)
