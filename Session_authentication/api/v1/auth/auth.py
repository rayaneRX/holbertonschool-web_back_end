#!/usr/bin/env python3
""" Module of Index views
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Auth Class """

    def __init__(self):
        """
            Constructor

            Args:
                path: path to authenticate
                excluded_paths: list of excluded path to authenticate
        """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
            Define which routes don't need authentication
        '''
        if path is None:
            return True

        if not excluded_paths or excluded_paths == []:
            return True

        for excluded_path in excluded_paths:
            if path.rstrip("/") == excluded_path.rstrip("/"):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Get the Authorization header from the request
        """
        if request is None:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current
        """
        return None

    def session_cookie(self, request=None):
        """
        Get the session cookie from the request
        """
        if request is None:
            return None

        session_cookie_name = getenv("SESSION_NAME", "_my_session_id")

        return request.cookies.get(session_cookie_name)
