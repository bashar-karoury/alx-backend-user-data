#!/usr/bin/env python3
"""
basic auth module to manage API authentication
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class to manage basic authentication mechanism"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header
        """
        # Return None if authorization_header is None
        # Return None if authorization_header is not a string
        # Return None if authorization_header doesn’t start by 'Basic '
        # Otherwise, return the value after Basic (after the space)
        # You can assume authorization_header contains only one Basic
        if not authorization_header or type(authorization_header) is not 'str':
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.strip('Basic ')
