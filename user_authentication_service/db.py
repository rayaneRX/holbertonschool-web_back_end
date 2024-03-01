#!/usr/bin/env python3
""" DB module """
from sqlite3 import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        
        Args:
            email: Email of the user.
            hashed_password: Hashed password of the user.
            
        Returns:
            User object that was added.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by the specified criteria
        
        Args:
            **kwargs: Arbitrary keyword arguments for filtering the user
            
        Returns:
            User object that matches the specified criteria
            
        Raises:
            NoResultFound: If no user is found with the specified criteria
            InvalidRequestError: If an invalid query argument is passed
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except InvalidRequestError:
            self._session.rollback()
            raise InvalidRequestError("Invalid query argument")
