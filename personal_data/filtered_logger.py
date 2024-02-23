#!/usr/bin/env python3
"""
 function called filter_datum that returns the log message obfuscate
"""


import logging
import csv
from typing import List

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Replace specified fields in the log message with the redaction string.
    Arguments:
        fields: List of strings representing fields to redact.
        redaction: String to use for redacting the fields.
        message: Log message containing the fields to be redacted.
        separator: String representing the separator between fields in the message.
    Returns:
        The log message with specified fields redacted.
    """
    pattern = fr'({"|".join(fields)})=[^{separator}]+'
    return re.sub(pattern, fr'\\1={redaction}', message)

PII_FIELDS = ("name", "email", "phone_number", "address", "credit_card")

def get_logger():
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

