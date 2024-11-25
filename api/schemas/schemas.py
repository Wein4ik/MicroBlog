from enum import Enum
from datetime import datetime
from pydantic import BaseModel, field_validator
from repository.models import ContentType


# class ContentType(Enum):
#     POST = 'post'
#     COMMENT = 'comment'


class CreateContentSchema(BaseModel):
    content: str
    content_type: ContentType
    user_id: int
    parent_id: int | None = None


class GetContentSchema(CreateContentSchema):
    id: int
    created_at: datetime


class CreateUserSchema(BaseModel):
    username: str

    @field_validator('username')
    @classmethod
    def username_length(cls, v: str) -> str:
        v = v.strip()  # Удаляем пробелы с начала и конца
        if not v:
            raise ValueError('Username cannot be empty or contain only spaces')
        if len(v) > 20:
            raise ValueError('Username must not exceed 20 characters')
        return v.lower()


class GetUserSchema(CreateUserSchema):
    id: int
    created_at: datetime
