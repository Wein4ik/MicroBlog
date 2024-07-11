class UserAlreadyExistsException(Exception):
    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundException(Exception):
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)


class ContentNotFoundException(Exception):
    def __init__(self, message="Content not found"):
        self.message = message
        super().__init__(self.message)


class LikeAlreadyExistsException(Exception):
    def __init__(self, message="Like already exists"):
        self.message = message
        super().__init__(self.message)
