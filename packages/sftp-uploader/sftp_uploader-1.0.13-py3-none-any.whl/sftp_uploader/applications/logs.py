"""
    Create a logger for package
"""


import logging

from sftp_uploader.constants.applications.logs import LOGGING_FORMAT


class CustomLogger(logging.Logger):
    """
        Custom class for logging in other classes
        
        Attributes:
            logger (logging.Logger): object logger
    """
    def __init__(self, 
                 logger_name: str) -> None:
        super().__init__(logger_name, 
                         level=logging.INFO,
                         )
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
        self.addHandler(stream_handler)
        
