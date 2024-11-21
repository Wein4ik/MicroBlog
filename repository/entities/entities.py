class UserEntity:
    def __init__(self, id, username, created_at, user=None):
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

    def model_dump(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at
        }


class LikeEntity:
    def __init__(self, id, user_id, content_id, like=None):
        self._id = id
        self.user_id = user_id
        self.content_id = content_id
        self._like = like

    @property
    def id(self):
        return self._id or self._like.id

    def model_dump(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content_id': self.content_id
        }


class ContentEntity:
    def __init__(self, id, content, created_at,
                 content_type, user_id, parent_id, _content=None):
        self._id = id
        self.content = content
        self._created_at = created_at
        self.content_type = content_type
        self.user_id = user_id
        self.parent_id = parent_id
        self._content = _content

    @property
    def id(self):
        return self._id or self._content.id

    @property
    def created_at(self):
        return self._created_at or self._content.created_at

    def model_dump(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at,
            'content_type': self.content_type,
            'user_id': self.user_id,
            'parent_id': self.parent_id
        }
