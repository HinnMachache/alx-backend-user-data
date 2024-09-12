#!/usr/bin/env python3
"""
Auth Module
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional


def _hash_password(password: str) -> bytes:
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
            hash_pw = _hash_password(password)
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

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """ Import statement of Optional"""
        """ gets a user based on Session ID
        Return:
            User if Session ID exists or None if not exist
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroys the Session ID
        Return:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
            return None
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """ Creates a user Token
        Return:
            Returns a str token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ Updates Password to new password and
        resets user token
        Return:
            None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pw = _hash_password(password)
            self._db.update_user(user.id, hashed_pw=hashed_pw,
                                 reset_token=None)
            return None
        except NoResultFound:
            raise ValueError
