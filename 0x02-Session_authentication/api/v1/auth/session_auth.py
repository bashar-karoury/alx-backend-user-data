#!/usr/bin/env python3
""" session auth module
"""
import uuid
from flask import request
from typing import List, TypeVar, Tuple
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ SessionAuth class to manage session authentication mechanism"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ method to create session for user based on user_id"""
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

# Create an instance method def user_id_for_session_id(self, session_id: str = None) -> str: that returns a User ID based on a Session ID:

# Return None if session_id is None
# Return None if session_id is not a string
# Return the value (the User ID) for the key session_id in the dictionary user_id_by_session_id.
# You must use .get() built-in for accessing in a dictionary a value based on key

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ retrives user_id from session_id"""
        if session_id is None or type(session_id) != str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)
