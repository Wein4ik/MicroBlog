from fastapi import APIRouter, HTTPException, Body
from starlette import status
from pydantic import BaseModel

from api.schemas.user_schemas import GetUserSchema, CreateUserSchema
from core.exceptions import UserAlreadyExistsException
from repository.sqlalchemy_repository import SQLAlchemyUserRepository
from repository.unit_of_work import UnitOfWork


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post('/create',
             status_code=status.HTTP_201_CREATED,
             response_model=GetUserSchema)
def add_user(user: CreateUserSchema):
    try:
        with UnitOfWork() as unit_of_work:
            repo = SQLAlchemyUserRepository(unit_of_work.session)
            user = repo.add(user.username)
            unit_of_work.commit()
            return user.model_dump()
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=e.message)
