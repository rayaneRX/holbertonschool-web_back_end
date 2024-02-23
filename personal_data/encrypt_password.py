#!/usr/bin/env python3
""" Module for implementing a hash_password function """
import bcrypt


def hash_password(password: str) -> bytes:
    """ Module for implementing a hash_password function """
    password_bytes = password.encode()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password
