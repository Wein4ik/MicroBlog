from abc import ABC, abstractmethod


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
    def update(self, user_id: int, **payload):
        pass

    @abstractmethod
    def delete(self, user_id: int):
        pass

    @abstractmethod
    def get_contents(self, user_id: int):
        pass

    @abstractmethod
    def get_likes(self, user_id: int):
        pass

# class ContentRepository(ABC):
#
#     @abstractmethod
