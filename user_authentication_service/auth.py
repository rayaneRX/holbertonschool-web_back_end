#!/usr/bin/env python3
""" Hash password """

from user import User
import bcrypt
import uuid

class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def register_user(self, email: str, password: str) -> User:
        # Check if user already exists
        if self._db.get_user_by_email(email):
            raise ValueError(f"User {email} already exists")

        # Hash the password
        hashed_password = self._hash_password(password)

        # Save the user to the database
        user = User(email, hashed_password)
        self._db.save_user(user)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        # Retrieve user by email
        user = self._db.get_user_by_email(email)

        if user:
            # Check if passwords match
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True

        return False

    def _generate_uuid() -> str:
        """
        Generates a new UUID and returns its string representation.
        """
        return str(uuid.uuid4())