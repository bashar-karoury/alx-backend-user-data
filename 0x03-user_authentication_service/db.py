#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import User, BaseModel as Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        """Add a user to the database
        """
        user = User()
        user.email = email
        user.hashed_password = hashed_password
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, *args, **kwargs) -> User:
        """ find first user with provided filter
            arguments
        """
        # Make sure that SQLAlchemy’s NoResultFound and InvalidRequestError
        # are raised when no results are found,
        # or when wrong query arguments are passed, respectively.
        for k, v in kwargs.items():
            # print(f'{k}: {v}')
            if not hasattr(User, k):
                raise InvalidRequestError(f"Invalid attribute: {k}")
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound("No user found with the given attributes")
        return user

    def update_user(self, id: int, *args, **kwargs) -> None:
        """updata user given its id and arbitrary attribute"""
        try:
            user = self.find_user_by(id=id)
            if user:
                for k, v in kwargs.items():
                    if not hasattr(User, k):
                        raise ValueError('value error')
                    user.__setattr__(k, v)
                self._session.add(user)
                self._session.commit()
            else:
                raise ValueError
        except ValueError:
            raise ValueError
