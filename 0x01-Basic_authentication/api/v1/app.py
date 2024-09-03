#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = os.getenv('AUTH_TYPE')
# Based on the environment variable AUTH_TYPE, load and assign the
# right instance of authentication to auth
if auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_type == 'basic':
    from api.v1.auth.auth import BasicAuth
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_authorized(error) -> str:
    """Not Authorized"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """No Access
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> None:
    """ Before request
    """
    paths = ['/api/v1/status/', '/api/v1/unauthorized/',
             '/api/v1/forbidden/']
    if not auth:
        return None
    if not auth.require_auth(request.path, paths):
        return None
    if not auth.authorization_header(request):
        abort(401)
    if not auth.current_user(request):
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host='0.0.0.0', port=5000)
