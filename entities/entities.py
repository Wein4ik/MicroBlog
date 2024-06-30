class UserEntity:
    def __init__(self, id, username, created_at, user):
        self._id = id
        self.username = username
        self._created_at = created_at
        self._user = user

    @property
    def id(self):
        return self._id or self._user.id

    @property
    def created_at(self):
        return self._created_at or self._user.created_at

    def dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at
        }
