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
