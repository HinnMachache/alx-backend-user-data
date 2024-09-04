#!/usr/bin/env python3
"""
A session class template
"""
from api.v1.auth.auth import Auth
from uuid import uuid4

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
