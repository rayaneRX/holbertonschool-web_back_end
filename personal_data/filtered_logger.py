#!/usr/bin/env python3
"""
 function called filter_datum that returns the log message obfuscate
"""


import re
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """"
    function called filter_datum that returns the log message obfuscate
	"""
    pattern = '|'.join(fields)
    return re.sub(r'(?<={}=)[^{}]+'.format(pattern, re.escape(separator)), redaction, message)

