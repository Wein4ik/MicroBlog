from core.exceptions import *
from repository.repository import UserRepository, ContentRepository, LikeRepository
from repository.models import *
from repository.entities.entities import *

from sqlalchemy.orm import Session

from repository.unit_of_work import UnitOfWork


class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, session: Session):
        self.session = session

    def _user_exist(self, **kwargs):
        return self.session.query(User).filter_by(**kwargs).first() is not None

    def add(self, username):
        if self._user_exist(username=username):
            raise UserAlreadyExistsException(message=f'User with username {username} is already exist')
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

    def is_user_existing(self, user_id):
        return self.session.query(User).filter_by(id=user_id).first() is not None

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


class SQLAlchemyContentRepository(ContentRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, content: str, content_type: ContentType, user_id: int, parent_id: int = None):
        with UnitOfWork() as unit_of_work:
            user_repo = SQLAlchemyUserRepository(unit_of_work.session)
            if not user_repo.is_user_existing(user_id):
                raise UserNotFoundException(f"User with id {user_id} not found")

        if parent_id is not None and not self.is_content_existing(parent_id):
            raise ContentNotFoundException(f"Parent with id {parent_id} not found")

        _content = Content(
            content=content,
            content_type=content_type,
            user_id=user_id,
            parent_id=parent_id
        )

        self.session.add(_content)
        return ContentEntity(**_content.dict(), _content=_content)

    def _get_by_id(self, content_id: int):
        content = self.session.query(Content).filter_by(id=content_id).first()
        return content

    def get_content(self, content_id: int):
        content = self._get_by_id(content_id)
        if content is None:
            raise ContentNotFoundException()

        return ContentEntity(**content.dict(), _content=content)

    def get_comments_on_post(self, post_id: int, limit: int = None):
        comments = (self.session.query(Content).
                    filter_by(parent_id=post_id).
                    all()
                    )
        comments_ent = [ContentEntity(**c.dict(), _content=c) for c in comments]
        if limit is not None:
            comments_ent = comments_ent[:limit]
        return comments_ent

    def delete(self, content_id: int):
        delete_content = self._get_by_id(content_id)
        if delete_content is None:
            raise ContentNotFoundException()

        self.session.delete(delete_content)

    def is_content_existing(self, content_id):
        return self.session.query(Content).filter_by(id=content_id).first() is not None


class SQLAlchemyLikeRepository(LikeRepository):

    def __init__(self, session: Session):
        self.session = session

    def _check_existence(self, user_id, content_id):
        like_record = self.session.query(Like).filter_by(user_id=user_id, content_id=content_id).first()
        return like_record

    def add(self, user_id, content_id):
        if self._check_existence(user_id, content_id):
            raise LikeAlreadyExistsException()

        user = self.session.query(User).filter_by(id=user_id).first()
        if not user:
            raise UserNotFoundException()

        content = self.session.query(Content).filter_by(id=content_id).first()
        if not content:
            raise ContentNotFoundException()

        like = Like(user_id=user_id, content_id=content_id)
        self.session.add(like)
        return LikeEntity(**like.dict(), like=like)

    def get_likes_by_user(self, user_id):
        _likes = self.session.query(Like).filter_by(user_id=user_id).all()
        likes = [LikeEntity(**like.dict(), like=like) for like in _likes]

        return likes

    def get_likes_by_content(self, content_id):
        _likes = self.session.query(Like).filter_by(content_id=content_id).all()
        likes = [LikeEntity(**like.dict(), like=like) for like in _likes]

        return likes
