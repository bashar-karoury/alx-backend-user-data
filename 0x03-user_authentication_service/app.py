#!/usr/bin/env python3
""" Flask App """
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth
from flask_cors import CORS
from typing import Any

AUTH = Auth()
app = Flask('main')
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def simple_route() -> None:
    """ simple route for root"""

    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> tuple[Any, int]:
    """ users post route"""

    form_email = request.form.get('email')
    form_pass = request.form.get('password')
    if not form_email or not form_pass:
        return jsonify({"message": "args provided are incorrect"}), 400
    try:
        user = AUTH.register_user(email=form_email, password=form_pass)
        print(user.email)
        return jsonify({"email": form_email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ login route"""

    form_email = request.form.get('email')
    form_pass = request.form.get('password')
    if not form_email or not form_pass:
        return jsonify({"message": "args provided are incorrect"}), 400
    if not AUTH.valid_login(email=form_email, password=form_pass):
        abort(401)
    sess_id = AUTH.create_session(form_email)
    resp = make_response(
        jsonify({"email": "<user email>", "message": "logged in"}), 200)
    resp.set_cookie('session_id', sess_id)
    return resp


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ logout route"""

    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ profile route"""

    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ get_reset_password_token route"""
    form_email = request.form.get('email')
    if not form_email:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(form_email)
        return jsonify({"email": form_email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
