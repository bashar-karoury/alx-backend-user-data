#!/usr/bin/env python3
""" Flask App """
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask('main')


@app.route('/')
def simple_route():
    return jsonify({"message": "Bienvenue"})

# The end-point should expect two form data fields: "email" and "password". If the user does not exist, the end-point should register it and respond with the following JSON payload:

# {"email": "<registered email>", "message": "user created"}
# If the user is already registered, catch the exception and return a JSON payload of the form

# {"message": "email already registered"}
# and return a 400 status code


@app.route('/users', methods=['POST', 'GET'])
def register_user():
    print(request.json())

    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
