#!/usr/bin/env python3
"""
basic auth module to manage API authentication
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class to manage basic authentication mechanism"""
    pass
