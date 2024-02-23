#!/usr/bin/env python3
"""
Personal data
"""

import re
import logging
from typing import List
from typing import Tuple
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection

PII_FIELDS: Tuple[str, str, str, str, str] = ("name", "email",
                                              "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Returns the log message obfuscated
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is
      separating all fields in the log line
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
        """Initializes a RedactingFormatter instance with a list
          of fields to obfuscate.

        Args:
            fields (List[str]): A list of strings representing
            the fields to obfuscate in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record, obfuscating specified fields
        in the log message.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log message.
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object named "user_data" with
       specified configurations.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """Returns a connector to the database.

    Returns:
        mysql.connector.connection.MySQLConnection: Database connector object.
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME', 'my_db')

    db = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

    return db


if __name__ == "__main__":
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")
    for row in cursor:
        print(row[0])
    cursor.close()
    db.close()*
