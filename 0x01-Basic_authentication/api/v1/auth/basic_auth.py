#!/usr/bin/env python3
"""
basic auth module to manage API authentication
"""
from flask import request
from typing import List, TypeVar, Tuple
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class to manage basic authentication mechanism"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header
        """
        # Return None if authorization_header is None
        # Return None if authorization_header is not a string
        # Return None if authorization_header doesn’t start by 'Basic '
        # Otherwise, return the value after Basic (after the space)
        # You can assume authorization_header contains only one Basic
        if not authorization_header or type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.strip('Basic ')

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ returns the decoded value of parameter str
        """
        # Return None if base64_authorization_header is None
        # Return None if base64_authorization_header is not a string
        # Return None if base64_authorization_header is not a valid Base64
        # Otherwise, return the decoded value as UTF8 string
        if (not base64_authorization_header or
                type(base64_authorization_header) is not str):
            return None
        try:
            import base64
            result = base64.b64decode(base64_authorization_header)
        except (Exception):
            return None
        return result.decode('utf-8')

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
            returns the user email and password from the Base64 decoded value.
        """

        # This method must return 2 values
        # Return None, None if parameter is None
        # Return None, None if parameter is not a string
        # Return None, None if parameter doesn’t contain ':'
        # Otherwise, return the user email and the user password
        if not decoded_base64_authorization_header:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if decoded_base64_authorization_header.find(':') == -1:
            return None, None
        result = decoded_base64_authorization_header.split(':')
        return result[0], result[1]
