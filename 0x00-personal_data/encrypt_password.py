#!/usr/bin/env python3
"""
    hashing passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
        expects one string argument name password and returns a salted,
        hashed password
    """
    password = password.encode('utf-8')
    # Hash a password for the first time, with a randomly-generated salt
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ validate that the provided password matches the hashed password"""
    return bcrypt.checkpw(password, hashed_password)
