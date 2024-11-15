#!/usr/bin/env python3
""" Module of Users views
"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
from api.v1.app import auth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ GET /api/v1/users
    Return:
      - list of all User objects JSON represented
    """
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    if not user_email or len(user_email) == 0:
        return jsonify({"error": "email missing"}), 400

    if not user_password or len(user_password) == 0:
        return jsonify({"error": "password missing"}), 400

    # get user of this provided email
    match_users = User.search({'email': user_email})
    user = match_users[0]
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user.is_valid_password(user_password):
        return jsonify({"error": "wrong password"}), 401

    # create session for this user
    session_id = auth.create_session(user.id)
    # Create a response object
    response = make_response(user.to_json())
    # Set a cookie
    cookie_name = os.getenv('SESSION_NAME')
    response.set_cookie(cookie_name, session_id)
    return response
