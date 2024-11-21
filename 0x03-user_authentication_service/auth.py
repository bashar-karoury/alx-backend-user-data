#!/usr/bin/env python3
""" auth module"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ return a salted hash of the input password hashed with bcrypt.hashpw
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)
