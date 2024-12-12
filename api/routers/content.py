from fastapi import APIRouter, HTTPException, Path
from typing import Annotated

from api.schemas.content_schemas import GetContentSchema, CreateContentSchema, ChangeTextContentSchema, \
    DeleteResponseSchema
from core.exceptions import ContentNotFoundException, UserNotFoundException
from repository.sqlalchemy_repository import SQLAlchemyContentRepository
from repository.unit_of_work import UnitOfWork
from starlette import status

router = APIRouter(
    prefix="/content",
    tags=["content"],
)


@router.get('/{content_id}', response_model=GetContentSchema)
def get_content(
        content_id: Annotated[int, Path(
            title="The ID of the item to get",
            ge=1,
            description="ID must be a positive integer greater than or equal to 1."
        )]):
    try:
        with UnitOfWork() as unit_of_work:
            repo = SQLAlchemyContentRepository(unit_of_work.session)
            content = repo.get_content(content_id)
        return content.model_dump()
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
            return content.model_dump()

    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ContentNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Server error")


@router.patch(
    path='/{content_id}/content_text',
    status_code=status.HTTP_200_OK,
    response_model=GetContentSchema
)
def update_content(
        content_id: Annotated[int, Path(
            title="The ID of the item to update",
            ge=1,
            description="ID must be a positive integer greater than or equal to 1."
        )],
        payload: ChangeTextContentSchema
):
    try:
        with UnitOfWork() as unit_of_work:
            repo = SQLAlchemyContentRepository(unit_of_work.session)
            content = repo.change_text(content_id, payload.content)

            unit_of_work.commit()
            return content.model_dump()
    except ContentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.delete(
    path='/{content_id}',
    status_code=status.HTTP_200_OK,
    response_model=DeleteResponseSchema
)
def delete_content(content_id: Annotated[int, Path(
    title="The ID of the item to update",
    ge=1,
    description="ID must be a positive integer greater than or equal to 1."
)]):
    try:
        with UnitOfWork() as unit_of_work:
            repo = SQLAlchemyContentRepository(unit_of_work.session)
            repo.delete_content(content_id)

            unit_of_work.commit()

            return DeleteResponseSchema(id=content_id)
    except ContentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
