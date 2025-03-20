from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services.objects.schemes.objects import ObjectsListRs, ObjectsCreateRs, ObjectsCreateRq
from services.objects.usecase.usecase import ObjectsUseCase
from core.postgres.access import get_async_session

router = APIRouter(
    prefix="/api/objects",
    tags=["objects"]
)


# Роутер для создания объекта
@router.post(
    "/create",
    status_code=200,
    response_model=ObjectsCreateRs
)
async def object_create(
        request: ObjectsCreateRq,
        db_session: AsyncSession = Depends(get_async_session),
) -> ObjectsCreateRs:
    use_case = ObjectsUseCase(db_session)
    try:
        response = await use_case.create(request)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    return response


# Роутер для получения списка объектов
@router.get(
    "/list",
    status_code=200,
    response_model=ObjectsListRs
)
async def objects_list(
        db_session: AsyncSession = Depends(get_async_session),
) -> ObjectsListRs:
    use_case = ObjectsUseCase(db_session)
    try:
        response = await use_case.list()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    return response
