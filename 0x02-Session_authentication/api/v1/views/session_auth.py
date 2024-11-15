#!/usr/bin/env python3
""" Module of Users views
"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /auth_session/login'
    """
    user_email = request.form.get('email')
    user_password = request.form.get('password')
    if not user_email or len(user_email) == 0:
        return jsonify({"error": "email missing"}), 400

    if not user_password or len(user_password) == 0:
        return jsonify({"error": "password missing"}), 400

    # get user of this provided email
    match_users = User.search({'email': user_email})
    user = match_users[0] if match_users else None
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


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ DELETE /api/v1/users
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)
