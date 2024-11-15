#!/usr/bin/env python3
""" session auth module
"""
from datetime import datetime, timedelta
import os
import uuid
from flask import request
from typing import List, TypeVar, Tuple
from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth
from models.user import User


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class to manage session with expiration authentication mechanism"""
    user_id_by_session_id = {}

    def __init__(self):
        """init method"""

        env_session_dur = os.getenv('SESSION_DURATION')
        if not env_session_dur:
            self.session_duration = int(env_session_dur)
        try:
            int(env_session_dur)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ method to create session for user based on user_id"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {}
        session_dictionary['user_id'] = user_id
        session_dictionary['created_at'] = datetime.datetime.now()
        SessionExpAuth.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ retrives user_id from session_id"""
        if session_id is None or type(session_id) != str:
            return None
        user_sess_dict = SessionAuth.user_id_by_session_id.get(session_id)
        if not user_sess_dict:
            return None
        if self.session_duration <= 0:
            return user_sess_dict['user_id']
        session_created_at = user_sess_dict.get('created_at')
        if not session_created_at:
            return None

        # Calculate expiration time
        expiration_time = session_created_at + \
            timedelta(seconds=self.session_duration)

        # Check if the session is expired
        if datetime.now() > expiration_time:
            return None
        return user_sess_dict['user_id']
