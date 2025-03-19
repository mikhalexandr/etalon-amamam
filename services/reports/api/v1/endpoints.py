from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from aiobotocore.session import get_session

from core.minio.access import get_minio
from core.postgres.access import get_async_session
from services.reports.schemes.reports import ReportsCreateRs, ReportsListRs, ReportsGetRs
from services.reports.usecase.usecase import ReportsUseCase
from core.settings import settings

router = APIRouter(
    prefix="/api/reports",
    tags=["reports"]
)


@router.post(
    "/create/{object_id}",
    status_code=200,
    response_model=ReportsCreateRs
)
async def report_create(
        object_id: str,
        files: List[UploadFile] = File(...),
        db_session: AsyncSession = Depends(get_async_session),
        minio_client: get_session = Depends(get_minio)
) -> ReportsCreateRs:
    use_case = ReportsUseCase(db_session, minio_client)
    try:
        response = await use_case.create(object_id, files)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    return response


@router.get(
    "/list/{object_id}",
    status_code=200,
    response_model=ReportsListRs
)
async def reports_list(
        object_id: str,
        db_session: AsyncSession = Depends(get_async_session),
        minio_client: get_session = Depends(get_minio)
) -> ReportsListRs:
    use_case = ReportsUseCase(db_session, minio_client)
    try:
        response = await use_case.list(object_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    return response


@router.get(
    "/get/{object_id}/{report_id}",
    status_code=200,
    response_model=ReportsGetRs
)
async def report_get(
        object_id: str,
        report_id: int,
        db_session: AsyncSession = Depends(get_async_session),
        minio_client: get_session = Depends(get_minio)
) -> ReportsGetRs:
    use_case = ReportsUseCase(db_session, minio_client)
    try:
        response = await use_case.get(object_id, report_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    return response


@router.get(
    "/download/{path}",
    status_code=200,
)
async def report_download(
        path: str,
        minio_client: get_session = Depends(get_minio)
) -> None:
    try:
        response = await minio_client.get_object(Bucket=settings.minio_bucket, Key=path)
        file_stream = response['Body']
        return StreamingResponse(file_stream, media_type='application/octet-stream', headers={
            "Content-Disposition": f"attachment; filename={path.split('/')[-1]}"
        })
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"File not found: {e}"
        )
