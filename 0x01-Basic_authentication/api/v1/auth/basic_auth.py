#!/usr/bin/env python3
from api.v1.auth.auth import Auth
from flask import request
from typing import List, TypeVar
import base64
from models.user import User


class BasicAuth(Auth):
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        returns the Base64 part of the Authorization header for a Basic Authentication:
        """
        if authorization_header is None or type(authorization_header) is not str:
            return None
        auth_head = authorization_header.split(' ')
        return auth_head[1] if auth_head[0] == 'Basic' else None    # return the value after Basic (after the space)

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        returns the decoded value of a Base64 string base64_authorization_header:
        """
        if base64_authorization_header is None or type(base64_authorization_header) is not str:
            return None
        try:
            base64_header = base64_authorization_header.encode('utf-8')
            base64_text = base64.b64decode(base64_header)
            message_text = base64_text.decode('utf-8')
            return message_text
        except Exception:
            return None
        
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value.
        """
        if (decoded_base64_authorization_header is None or type(decoded_base64_authorization_header) is not str
            or ":" not in decoded_base64_authorization_header):
            return (None, None)
        user_email, user_password = decoded_base64_authorization_header.split(':')
        return (user_email, user_password)
    
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        if (not user_email or not(isinstance(user_email, str)) or not user_pwd or
            not(isinstance(user_pwd, str))):
            return None
        
        users = User.search({'email': user_email})
        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ overloads Auth and
            retrieves the User instance for a request
        """
        try:
            header = self.authorization_header(request)
            base64_h = self.extract_base64_authorization_header(header)
            decode_h = self.decode_base64_authorization_header(base64_h)
            credents = self.extract_user_credentials(decode_h)
            return self.user_object_from_credentials(credents[0], credents[1])
        except Exception:
            return None
