#!/usr/bin/env python3
""" Flask App """
from flask import Flask, jsonify, request
from auth import Auth
from flask_cors import CORS
from typing import Any

AUTH = Auth()
app = Flask('main')
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.route('/')
def simple_route() -> None:
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user_route() -> tuple[Any, int]:
    form_email = request.form.get('email')
    form_pass = request.form.get('password')
    # data = request.get_json()
    # email = data.get('email')
    # password = data.get('password')
    if not form_email or not form_pass:
        return jsonify({"message": "args provided are incorrect"}), 400
    try:
        user = AUTH.register_user(email=form_email, password=form_pass)
        return jsonify({"email": form_email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
