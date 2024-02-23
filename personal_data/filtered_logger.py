#!/usr/bin/env python3
"""
Main file
"""

import os
import mysql.connector


def get_db():
    """Returns a connector to the MySQL database."""
    # Retrieve database credentials from environment variables
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    # Connect to the database
    return mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=db_name
    )


if __name__ == "__main__":
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")
    for row in cursor:
        print(row[0])
    cursor.close()
    db.close()
