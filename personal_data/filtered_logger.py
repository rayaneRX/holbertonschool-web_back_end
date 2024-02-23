#!/usr/bin/env python3
"""
Function called filter_datum that returns the log message obfuscated.
"""

import logging
from logging import StreamHandler
from typing import List
import csv
from datetime import datetime
import re  # Added import for regular expressions

# Define PII_FIELDS before usage
PII_FIELDS = ("name", "email", "phone", "address", "credit_card")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Replace specified fields in the log message with the redaction string.
    """
    return re.sub(fr'({"|".join(fields)})=[^{separator}]+',
                  fr'\1={redaction}',
                  message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format the log record. """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """Return a logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handler = StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


if __name__ == "__main__":
    logger = get_logger()
    logger.info("This is a test message with sensitive information: "
                "name=John; email=john@example.com; phone=123456789; "
                "address=123 Street; credit_card=1234567890123456")
