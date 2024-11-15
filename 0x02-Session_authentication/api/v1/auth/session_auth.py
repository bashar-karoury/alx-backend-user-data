#!/usr/bin/env python3
""" session auth module
"""
from flask import request
from typing import List, TypeVar, Tuple
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ SessionAuth class to manage session authentication mechanism"""
    pass
