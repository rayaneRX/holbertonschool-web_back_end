#!/usr/bin/env python3
"""
 function called filter_datum that returns the log message obfuscate
"""

import logging
from typing import List
from filtered_logger import filter_datum
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:

    """
    function called filter_datum that returns the log message obfuscate
    """

    pattern = '|'.join(fields)
    return re.sub(r'({})=([^{}]+)'.format(pattern, re.escape(separator)),
                  r'\1={}'.format(redaction), message)




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
