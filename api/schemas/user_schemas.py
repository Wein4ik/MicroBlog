from datetime import datetime

from pydantic import BaseModel, field_validator

from config import USERNAME_MAX_LENGTH_DEFAULT


class CreateUserSchema(BaseModel):
    username: str

    @field_validator('username')
    @classmethod
    def username_length(cls, v: str) -> str:
        v = v.strip()  # Удаляем пробелы с начала и конца
        if not v:
            raise ValueError('Username cannot be empty or contain only spaces')
        if len(v) > USERNAME_MAX_LENGTH_DEFAULT:
            raise ValueError('Username must not exceed 20 characters')
        return v.lower()


class GetUserSchema(CreateUserSchema):
    id: int
    created_at: datetime
