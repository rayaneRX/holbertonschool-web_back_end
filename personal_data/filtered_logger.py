#!/usr/bin/env python3
"""
Filtered logger module
"""

import logging
import csv
from typing import List
from logging import Logger, StreamHandler

# Define PII_FIELDS constant
PII_FIELDS = ("name", "email", "phone", "address", "creditcard")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscate sensitive information from log message
    """
    return re.sub(fr'({"|".join(fields)})=[^{separator}]+',
                  fr'\1={redaction}',
                  message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Args:
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format the log record.
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> Logger:
    """
    Returns a configured logger object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False  # Do not propagate messages to other loggers
    return logger


if __name__ == "__main__":
    logger = get_logger()
    logger.info("This is a test message with sensitive information: "
                "name=bob; email=bob@example.com; phone=123456789; "
                "address=123 Street; creditcard=1234567890123456")
