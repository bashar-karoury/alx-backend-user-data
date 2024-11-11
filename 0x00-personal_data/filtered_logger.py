#!/usr/bin/env python3
"""
Regex-ing
"""
import os
import logging
import re
from typing import List
import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector import connect


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
        returns the log message obfuscated
    """
    for field in fields:
        pattern = rf"(?<=\b{field}\b=).*?(?={separator})"
        message = re.sub(pattern, redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ initialization method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format method to obfuscate PII info before logging"""
        record.msg = filter_datum(self.fields,
                                  self.REDACTION,
                                  record.msg,
                                  self.SEPARATOR)
        return super().format(record)


# name,email,phone,ssn,password,ip,last_login,user_agent
PII_FIELDS = ('email', 'user_agent', 'ssn', 'password', 'ip')


def get_logger() -> logging.Logger:
    """ returns logger with a StreamHandler that has
        RedactingFormatter as formatter
    """
    logger = logging.getLogger("user_data")
    # It should not propagate messages to other loggers.
    logger.propagate = False
    # It should have a StreamHandler with RedactingFormatter as formatter.
    stream = logging.StreamHandler()
    formatter = RedactingFormatter([])
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    logger.setLevel(logging.INFO)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
        returns a connector to the database specified by credentials saved
        as environment variables
    """
    host = os.getenv('PERSONAL_DATA_DB_HOST')
    user = os.getenv('PERSONAL_DATA_DB_USERNAME')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD')
    database = os.getenv('PERSONAL_DATA_DB_NAME')
    connection = mysql.connector.connect(
        host, user, password, database
    )
    return connection


def main() -> None:
    """
        obtain a database connection using get_db and retrieve all rows
        in the users table and display each row under a filtered format
    """
    db = get_db()

    cursor = db.cursor()
    cursor.execute("SELECT COUNT* FROM users;")
    result = cursor.fetchall()
    fields = ['name'
              'email',
              'phone',
              'ssn',
              'password']
    for row in result:
        print(filter_datum(fields, '***', str(row), ';'))
    cursor.close()
    db.close()
