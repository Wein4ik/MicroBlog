from fastapi import APIRouter, HTTPException

from api.schemas import GetContentSchema, CreateContentSchema
from app.exceptions import ContentNotFoundException
from repository.sqlalchemy_repository import SQLAlchemyContentRepository
from repository.unit_of_work import UnitOfWork
from starlette import status

router = APIRouter(
    prefix="/content",
    tags=["content"],
)


@router.get('/{content_id}', response_model=GetContentSchema)
def get_content(content_id: int):
    try:
        with UnitOfWork() as unit_of_work:
            repo = SQLAlchemyContentRepository(unit_of_work.session)
            content = repo.get_content(content_id)
        return content.dict()
    except ContentNotFoundException as e:
        raise HTTPException(status_code=404, detail=f"Content with ID {content_id} not found")


@router.post('',
             status_code=status.HTTP_201_CREATED,
             response_model=GetContentSchema)
def create_content(payload: CreateContentSchema):
    try:
        with UnitOfWork() as unit_of_work:
            repo = SQLAlchemyContentRepository(unit_of_work.session)
            content = repo.add(**payload.dict())
            unit_of_work.commit()
            return content.dict()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Server error")

