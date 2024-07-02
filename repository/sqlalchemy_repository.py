from app.exceptions import UserAlreadyExistsException, UserNotFoundException
from repository.repository import UserRepository
from repository.models import *
from entities.entities import *

from sqlalchemy.orm import Session


class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, session: Session):
        self.session = session

    def _user_exist(self, **kwargs):
        return self.session.query(User).filter_by(**kwargs).first() is not None

    def add(self, username):
        if self._user_exist(username=username):
            raise UserAlreadyExistsException(message='Пользователь с таким username уже существует')
        user = User(username=username)
        self.session.add(user)
        return UserEntity(**user.dict(), user=user)

    def _get_by_id(self, user_id: int):
        user = self.session.query(User).filter_by(id=user_id).first()
        return user

    def _get_by_username(self, username: int):
        user = self.session.query(User).filter_by(username=username).first()
        return user

    def users_list(self, limit: int = None, **filters):
        query_users = (self.session.query(User).
                       filter_by(**filters).limit(limit).all())
        users = [UserEntity(**user.dict(), user=user) for user in query_users]
        return users

    def update(self, user_id: int, **payload):
        user = self._get_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        for key, value in payload.items():
            setattr(user, key, value)

        self.session.add(user)

        return UserEntity(**user.dict(), user=user)

    def delete(self, user_id):
        user = self._get_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        self.session.delete(user)

    def get_id_by_username(self, username: str):
        return self.session.query(User.id).filter_by(username=username).first()[0]

    def get_contents(self, user_id: int):
        cons = self.session.query(User).filter_by(id=user_id).first().contents
        return [ContentEntity(**c.dict(), cont=c) for c in cons]

    def get_likes(self, user_id: int):
        likes = self.session.query(User).filter_by(id=user_id).first().likes
        return [LikeEntity(**like.dict(), like=like) for like in likes]
