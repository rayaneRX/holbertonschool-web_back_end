#!/usr/bin/env python3
""" Module for implementing a hash_password function """
import bcrypt


def hash_password(password: str) -> bytes:
    """ Module for implementing a hash_password function """
    password_bytes = password.encode()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Module for implementing a is_valid function """
    password_bytes = password.encode()
    return bcrypt.checkpw(password_bytes, hashed_password)


if __name__ == "__main__":
    password = "MyAmazingPassw0rd"
    encrypted_password = hash_password(password)
    print(encrypted_password)
    print(is_valid(encrypted_password, password))
