#!/usr/bin/env python3
""" Flask App """
from flask import Flask, jsonify

app = Flask('main')


@app.route('/')
def simple_route():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST', 'GET'])
def register_user():
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
