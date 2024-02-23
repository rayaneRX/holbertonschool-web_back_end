#!/usr/bin/env python3
"""
 function called filter_datum that returns the log message obfuscate
"""


import logging
import csv

PII_FIELDS = ("name", "email", "phone", "address", "creditcard")


class RedactingFormatter(logging.Formatter):
    def __init__(self, fields):
        super().__init__()
        self.fields = fields

    def format(self, record):
        message = super().format(record)
        for field in self.fields:
            message = message.replace(field, "****")
        return message


def get_logger():
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger


if __name__ == "__main__":
    logger = get_logger()
    logger.info("This is a test message with sensitive information: "
                "name=bob; email=bob@example.com; phone=123456789; "
                "address=123 Street; creditcard=1234567890123456")
