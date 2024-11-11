#!/usr/bin/env python3
"""
Regex-ing
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
        returns the log message obfuscated
    """
    for field in fields:
        pattern = rf"(?<={field}=).*?(?=,|\.|{separator})"
        # Perform the replacement
        message = re.sub(pattern, redaction, message)
    return message
