#!/usr/bin/env python3

from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    """ GET route index
    Return:
        {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """ POST route request
    Return:
        "message": "email already registered" if user exists
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST route request
    Return:
        {"email": "<user email>", "message": "logged in"}
        if user exists
    """
    email = request.form.get("email")
    password = request.form.get("password")
    user_login = AUTH.valid_login(email, password)
    if user_login:
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({f"email": f"{email}", "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
