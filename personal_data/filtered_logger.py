#!/usr/bin/python3
"""
 function called filter_datum that returns the log message obfuscate
"""


import re

def filter_datum(fields, redaction, message, separator):
    """
    function called filter_datum that returns the log message obfuscate
	"""
    return re.sub(r'(?<=^|[' + re.escape(separator) + r'])(' + '|'.join(fields) + r')=[^;]+', redaction, message)
