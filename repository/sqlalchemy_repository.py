from repository.repository import UserRepository
from app.models import *
from sqlalchemy.orm import Session


class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, **kwargs):
        user = User(**kwargs)
        self.session.add(user)
        self.session.commit()

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
        self.session.commit()

        return user

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
