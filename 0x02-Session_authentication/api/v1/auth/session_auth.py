#!/usr/bin/env python3
"""
session auth module to manage Session API authentication
"""
from flask import request
from typing import List, TypeVar, Tuple
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ SessionAuth class to manage session authentication mechanism"""
    pass
    # def extract_base64_authorization_header(
    #         self, authorization_header: str) -> str:
    #     """returns the Base64 part of the Authorization header
    #     """
    #     # Return None if authorization_header is None
    #     # Return None if authorization_header is not a string
    #     # Return None if authorization_header doesn’t start by 'Basic '
    #     # Otherwise, return the value after Basic (after the space)
    #     # You can assume authorization_header contains only one Basic
    #     if not authorization_header or type(authorization_header) is not str:
    #         return None
    #     if not authorization_header.startswith('Basic '):
    #         return None
    #     return authorization_header.strip('Basic ')

    # def decode_base64_authorization_header(
    #         self, base64_authorization_header: str) -> str:
    #     """ returns the decoded value of parameter str
    #     """
    #     # Return None if base64_authorization_header is None
    #     # Return None if base64_authorization_header is not a string
    #     # Return None if base64_authorization_header is not a valid Base64
    #     # Otherwise, return the decoded value as UTF8 string
    #     if (not base64_authorization_header or
    #             type(base64_authorization_header) is not str):
    #         return None
    #     try:
    #         import base64
    #         result = base64.b64decode(base64_authorization_header)
    #     except (Exception):
    #         return None
    #     return result.decode('utf-8')

    # def extract_user_credentials(
    #         self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
    #     """
    #         returns the user email and password from the Base64 decoded value.
    #     """

    #     # This method must return 2 values
    #     # Return None, None if parameter is None
    #     # Return None, None if parameter is not a string
    #     # Return None, None if parameter doesn’t contain ':'
    #     # Otherwise, return the user email and the user password
    #     if not decoded_base64_authorization_header:
    #         return None, None
    #     if type(decoded_base64_authorization_header) is not str:
    #         return None, None
    #     if decoded_base64_authorization_header.find(':') == -1:
    #         return None, None
    #     result = decoded_base64_authorization_header.split(':', 1)
    #     return result[0], result[1]

    # def user_object_from_credentials(
    #         self, user_email: str, user_pwd: str) -> TypeVar('User'):
    #     """ returns the User instance based on his email and password
    #     """

    #     # Return None if user_email is None or not a string
    #     # Return None if user_pwd is None or not a string
    #     # Return None if your database (file) doesn’t contain the user
    #     # Return None if user_pwd is not the password of the User
    #     # Otherwise, return the User instance
    #     if not user_email or type(user_email) is not str:
    #         return None
    #     if not user_pwd or type(user_pwd) is not str:
    #         return None
    #     users = User.search({"email": user_email})
    #     # print('users: ', users)
    #     if not users:
    #         return None
    #     for user in users:
    #         if user.is_valid_password(user_pwd):
    #             return user
    #     return None

    # def current_user(self, request=None) -> TypeVar('User'):
    #     """retrieves the User instance for a request
    #     """

    #     # You must use authorization_header
    #     auth_header = self.authorization_header(request=request)
    #     # You must use extract_base64_authorization_header
    #     base_64_encoded = self.extract_base64_authorization_header(auth_header)
    #     # You must use decode_base64_authorization_header
    #     decoded_header = self.decode_base64_authorization_header(
    #         base_64_encoded)
    #     # You must use extract_user_credentials
    #     usr_email, usr_pwd = self.extract_user_credentials(decoded_header)
    #     # You must use user_object_from_credentials
    #     return self.user_object_from_credentials(usr_email, usr_pwd)
