from abc import ABC, abstractmethod


class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self, user_id: int):
        pass

    @abstractmethod
    def add(self, **kwargs):
        pass

    @abstractmethod
    def get_by_username(self, username: str):
        pass

    @abstractmethod
    def users_list(self, limit: int = None, **filters):
        pass

    @abstractmethod
    def update(self, user_id: int, **payload):
        pass

    @abstractmethod
    def delete(self, user_id):
        pass
