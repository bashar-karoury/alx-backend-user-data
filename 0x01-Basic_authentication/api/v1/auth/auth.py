#!/usr/bin/env python3
"""
auth module to manage API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Main class of Auth to managem authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns True if path is not one of excluded_paths, False otherwise
        """
        if not path:
            return True
        if len(excluded_paths) == 0:
            return True
        slashed_path = path + '/' if path[-1] != '/' else path
        if slashed_path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ returns None - request will be the Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None - request will be the Flask request object
        """
        return None
