#!/usr/bin/env python3
from flask import request
from typing import List, TypeVar


class Auth:
    """
    This class is the template for all authentication system to be implemented.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns returns True if the path is not in
        the list of strings excluded_paths:
        """
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True
        if path[-1] != '/':
            path += '/'         # Slash Tolerant
        for p in excluded_paths:
            if p.endswith('*'):
                if path.startswith(p[:1]):
                    return False
        return False if path in excluded_paths else True

    def authorization_header(self, request=None) -> str:
        """
        Returns None if request is does not contain header key Authorization
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user method"""
        return None
