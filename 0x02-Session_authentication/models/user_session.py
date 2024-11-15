#!/usr/bin/env python3
""" User module
"""
import hashlib
from models.base import Base


class UserSession(Base):
    """ User class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User instance
        """
        super().__init__(*args, **kwargs)
        # print("kwargs", **kwargs)
        print(f"created user id: {kwargs.get('user_id')}")
        print(f"created session_id: {kwargs.get('session_id')}")
        print(f"created created at{kwargs.get('session_created_at')}")
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        self.session_created_at = kwargs.get('session_created_at')
