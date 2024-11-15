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
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user import User
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class to manage session with exp auth mechanism
        with session saved in db for persistent storage"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ method to create session for user based on user_id"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        # save it to database
        usr_session = UserSession(
            session_id=session_id,
            user_id=user_id,
            session_created_at=datetime.now())
        usr_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ retrives user_id from session_id"""
        if session_id is None or type(session_id) != str:
            return None
        UserSession.load_from_file()
        # search for session_id
        user_sessions = UserSession.search({'session_id': session_id})
        print(f'user_sessions: {user_sessions}')
        if not user_sessions:
            return None
        user_session = user_sessions[0]
        if not user_session:
            return None
        if self.session_duration <= 0:
            return user_session.user_id
        session_created_at = user_session.session_created_at
        print('debugging')
        print(session_created_at)
        print(type(session_created_at))
        if not session_created_at:
            return None

        # Convert session_created_at from str to datetime object
        if isinstance(session_created_at, str):
            session_created_at = datetime.strptime(
                session_created_at, "%Y-%m-%dT%H:%M:%S")
        expiration_time = session_created_at + \
            timedelta(seconds=self.session_duration)

        # Check if the session is expired
        if datetime.now() > expiration_time:
            print('Expired')
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """ destroys the UserSession based on the Session ID from the
            request cookie/ logout
        """
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        # search for session_id
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None
        # user_sess_dict = SessionExpAuth.user_id_by_session_id.get(session_id)
        user_session = user_sessions[0]
        if not user_session:
            return None
        user_session.remove()
        return True
