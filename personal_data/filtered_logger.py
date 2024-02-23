#!/usr/bin/env python3
"""
 function called filter_datum that returns the log message obfuscate
"""

import logging
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
    pdate the class to accept a list of strings fields constructor argument.
    """
    pattern = fr'({"|".join(fields)})=[^{separator}]+'
    return re.sub(pattern, fr'\\1={redaction}', message)
