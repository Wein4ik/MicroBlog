from enum import Enum
from datetime import datetime
from pydantic import BaseModel
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


class GetUserSchema(CreateUserSchema):
    id: int
    created_at: datetime
