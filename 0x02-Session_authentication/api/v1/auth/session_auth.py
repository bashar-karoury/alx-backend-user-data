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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ retrives user_id from session_id"""
        if session_id is None or type(session_id) != str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a user instance based on a cookie value"""
        seesion_id = self.session_cookie(request)
        print(f'session_id: {seesion_id}')
        user_id = self.user_id_for_session_id(seesion_id)
        print(f'user_id: {user_id}')
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """ deleted user session / logout"""
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del SessionAuth.user_id_by_session_id[session_id]
        return True
