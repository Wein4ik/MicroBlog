from fastapi import APIRouter, HTTPException
from starlette import status

from core.exceptions import UserAlreadyExistsException
from repository.sqlalchemy_repository import SQLAlchemyUserRepository
from repository.unit_of_work import UnitOfWork

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post('/create',
             status_code=status.HTTP_201_CREATED)
def add_user(username: str):
    try:
        with UnitOfWork() as unit_of_work:
            repo = SQLAlchemyUserRepository(unit_of_work.session)
            user = repo.add(username)
            unit_of_work.commit()
            return user.dict()
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))
