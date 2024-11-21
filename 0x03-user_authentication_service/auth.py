#!/usr/bin/env python3
""" auth module"""
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _generate_uuid() -> str:
    """ generates random number as string """
    return str(uuid.uuid4())


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
            return bcrypt.checkpw(
                password.encode('utf-8'),
                user.hashed_password)

        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ create a session_id for user associated with provided email
            and return it"""

        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ takes a single session_id string argument and returns
            the corresponding User or None """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """method updates the corresponding user’s session ID to None."""
        try:
            self._db.update_user(user_id, session_id=None)

        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ returns resest password token"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = str(uuid.uuid4())
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ update user password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(
                user.id,
                hashed_password=_hash_password(password),
                reset_token=None)
        except NoResultFound:
            raise ValueError
