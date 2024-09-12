#!/usr/bin/env python3
"""
Flask APP
"""
from flask import Flask, jsonify, request, abort
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ DELETE route request, Implement LogOut
    Destroys the User Session ID
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ GET User profile
    Return:
        {"email": "<user email>"}
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_flushes=False)
def get_reset_password_token() -> str:
    """ Reset password token if user exists
    Return:
        {"email": "<user email>", "reset_token": "<reset token>"}"""
    email = request.form.get("email")
    user = AUTH.create_session(email)
    if not user:
        abort(403)
    else:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"}), 200


@app.route('/reset_password', methods=['PUT'], strict_flushes=False)
def update_password():
    """ Updates Password if token is valid
    Return:
        {"email": "<user email>", "message": "Password updated"}
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    json_f = jsonify({"email": f"{email}", "message": "Password updated"})
    try:
        AUTH.update_password(reset_token, new_password)
        return json_f, 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
