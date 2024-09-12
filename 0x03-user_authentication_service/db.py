#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
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
        """Memorized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Saves user to the database
        """
        if not email or not hashed_password:
            return
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        # change import statement -> from from sqlalchemy.orm.exc
        # import NoResultFound, InvalidRequestError
        """ Find User by some arguments
        Return:
            User
        """
        session = self._session
        try:
            user_filtered = session.query(User).filter_by(**kwargs).first()
            if user_filtered is None:
                raise NoResultFound()
            return user_filtered
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates User based on an Attirbute
        Arguments:
            user_id:
                pecific user to be updated
        """
        attributes = User.__table__._columns.keys()
        user_return = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key not in attributes:
                raise ValueError
            setattr(user_return, key, value)
        self._session.commit()
        return None
