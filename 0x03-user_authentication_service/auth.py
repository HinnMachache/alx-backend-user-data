#!/usr/bin/env python3

from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.exc import NoResultFound


def _hashed_password(password: str) -> bytes:
    """ Generate user's hashed password
    Return:
        User's hashed password
    """
    hashed_password = hashpw(password.encode('utf-8'), gensalt())
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers user if the user does not exist"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hash_pw = _hashed_password(password)
            new_user = self._db.add_user(email, hash_pw)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ Checks if user exists and allow user
        to sign in
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return checkpw(password.encode('utf-8'), user.hashed_password)

    def _generate_uuid(self) -> str:
        """ Returns a unique ID
        """
        return str(uuid4())

    def create_session(self, email: str) -> str:
        """ Creates a user session id
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)

        return session_id
