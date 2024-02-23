import re
from typing import List
import logging
def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Replace specified fields in the log message with the redaction string.
    fields: List of strings representing fields to redact.
    redaction: String to use for redacting the fields.
    message: Log message containing the fields to be redacted.
    separator: String representing the separator between fields in the message.
    Returns:
        The log message with specified fields redacted.
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
        """ Initialize the RedactingFormatter instance.
        Args:
            fields (List[str]): List of fields to redact in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format the log record.
        Args:
            record (logging.LogRecord): Log record to be formatted.
        Returns:
            str: Formatted log message.
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
