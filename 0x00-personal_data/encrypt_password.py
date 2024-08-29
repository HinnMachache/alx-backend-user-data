#!/usr/bin/env python3

import bcrypt


def hash_password(password):
    """
    returns a salted, hashed password, which is a byte string.
    """
    if password:
        password = password.encode('utf-8')  # Convert to Byte
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validate that the provided password matches the hashed password.
    """
    if hashed_password and password:
        return bcrypt.checkpw(str.encode(password), hashed_password)
