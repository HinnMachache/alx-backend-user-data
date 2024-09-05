#!/usr/bin/env python3
"""
A session class template
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
import os
from models.user import User


class SessionAuth(Auth):
    """ Session Auth Template
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id
        """
        if user_id is None or not(isinstance(user_id, str)):
            return None

        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User ID based on a Session ID:
        """
        if not(session_id) or not(isinstance(session_id, str)):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a User instance based on a cookie value:
        """
        return User.get(
                self.user_id_for_session_id(self.session_cookie(request)))

    def destroy_session(self, request=None):
        """Delete the user session / log out
        """
        if request:
            session_id = self.session_cookie(request)
            if not session_id:
                return False
            if not self.user_id_for_session_id(session_id):
                return False
            self.user_id_by_session_id.pop(session_id)
            return True

    def destroy_session(self, request=None):
        """Delete the user session / log out
        """
        if request:
            session_id = self.session_cookie(request)
            if not session_id:
                return False
            if not self.user_id_for_session_id(session_id):
                return False
            self.user_id_by_session_id.pop(session_id)
            return True
