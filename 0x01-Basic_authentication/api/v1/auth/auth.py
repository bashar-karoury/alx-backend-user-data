#!/usr/bin/env python3
"""
auth module to manage API authentication
"""
from flask import request
from typing import List


class Auth:
    """ Main class of Auth to managem authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ returns None - request will be the Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None - request will be the Flask request object
        """
        return None
