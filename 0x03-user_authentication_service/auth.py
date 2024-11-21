#!/usr/bin/env python3
""" auth module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ return a salted hash of the input password hashed with bcrypt.hashpw
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register user in the authentication system"""
        # check if there is a user is already exist with the
        # provided email
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')

        except NoResultFound:
            hashed_pass = _hash_password(password)
            return self._db.add_user(email=email, hashed_password=hashed_pass)

    def valid_login(self, email: str, password: str) -> bool:
        """ validate login info"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

        except NoResultFound:
            return False
