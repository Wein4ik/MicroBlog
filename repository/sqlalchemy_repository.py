from app.exceptions import UserAlreadyExistsException
from repository.repository import UserRepository
from repository.models import *
from entities.entities import UserEntity

from sqlalchemy.orm import Session


class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, session: Session):
        self.session = session

    def _user_exist(self, username):
        return self.session.query(User).filter_by(username=username).first() is not None

    def add(self, username):
        if self._user_exist(username):
            raise UserAlreadyExistsException(message='Пользователь с таким username уже существует')
        user = User(username=username)
        self.session.add(user)
        return UserEntity(**user.dict(), user=user)

    def get_by_id(self, user_id: int):
        user = self.session.query(User).filter_by(id=user_id).first()
        return user

    def get_by_username(self, username: int):
        user = self.session.query(User).filter_by(username=username).first()
        return user

    def users_list(self, limit: int = None, **filters):
        users = (self.session.query(User).
                 filter_by(**filters).limit(limit).all())
        return users

    def update(self, user_id: int, **payload):
        user = self.get_by_id(user_id)
        if not user:
            return None

        for key, value in payload.items():
            setattr(user, key, value)

        self.session.add(user)

        return user

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        if user:
            self.session.delete(user)
