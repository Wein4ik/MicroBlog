from abc import ABC, abstractmethod

from repository.models import ContentType


class UserRepository(ABC):

    @abstractmethod
    def add(self, **kwargs):
        pass

    @abstractmethod
    def get_id_by_username(self, username: str):
        pass

    @abstractmethod
    def users_list(self, limit: int = None, **filters):
        pass

    @abstractmethod
    def update(self, user_id, **payload):
        pass

    @abstractmethod
    def delete(self, user_id):
        pass

    @abstractmethod
    def get_contents(self, user_id):
        pass

    @abstractmethod
    def get_likes(self, user_id):
        pass


class ContentRepository(ABC):

    @abstractmethod
    def add(self, text: str, content_type: ContentType, user_id, parent_id: int = None):
        pass

    @abstractmethod
    def get_content(self, content_id: int):
        pass

    @abstractmethod
    def get_comments_on_post(self, post_id, limit: int = None):
        pass

    @abstractmethod
    def delete(self, content_id):
        pass


class LikeRepository(ABC):

    @abstractmethod
    def add(self, user_id, content_id):
        pass

    @abstractmethod
    def get_likes_by_user(self, user_id):
        pass

    @abstractmethod
    def get_likes_by_content(self, content_id):
        pass
