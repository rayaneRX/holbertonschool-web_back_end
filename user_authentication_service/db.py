#!/usr/bin/env python3

"""DB module"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

Base = declarative_base()

class User(Base):
    """User class"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by a given attribute."""
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise ValueError("User not found")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user by a given attribute."""
        user = self._session.query(User).filter_by(id=user_id).first()
        if user is None:
            raise ValueError("User not found")
        for key, value in kwargs.items():
            setattr(user, key, value)
        self._session.commit()

if __name__ == "__main__":
    my_db = DB()

    # Add a user
    user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
    print("User added:", user_1.id)

    # Find a user
    try:
        find_user = my_db.find_user_by(email="test@test.com")
        print("Found user:", find_user.id)
    except ValueError as e:
        print(e)

    # Update a user
    try:
        my_db.update_user(user_1.id, hashed_password="NewSuperHashedPwd")
        print("Password updated")
    except ValueError as e:
        print(e)
