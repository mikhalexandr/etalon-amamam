from typing import List

import redis.asyncio as redis
from inference_sdk import InferenceHTTPClient

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from core.minio.access import get_minio_client
from core.postgres.access import get_async_session
from core.redis.access import get_redis
from core.roboflow.access import get_roboflow
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
        redis_client: redis.Redis = Depends(get_redis),
        roboflow_client: InferenceHTTPClient = Depends(get_roboflow)
) -> ReportsCreateRs:
    use_case = ReportsUseCase(db_session, redis_client, roboflow_client)
    response = await use_case.create(object_id, files)
    return response


@router.get(
    "/list/{object_id}",
    status_code=200,
    response_model=ReportsListRs
)
async def reports_list(
        object_id: str,
        db_session: AsyncSession = Depends(get_async_session),
) -> ReportsListRs:
    use_case = ReportsUseCase(db_session)
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
        db_session: AsyncSession = Depends(get_async_session)
) -> ReportsGetRs:
    use_case = ReportsUseCase(db_session)
    try:
        response = await use_case.get(object_id, report_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    return response


@router.get(
    "/download/{path:path}",
    status_code=200,
)
async def download_file(
        path: str,
) -> Response:
    try:
        minio_client = await get_minio_client()
        async with minio_client as client:
            response = await client.get_object(Bucket=settings.minio_bucket, Key=path)
            file_content = await response['Body'].read()
            headers = {
                "Content-Disposition": f"attachment; filename={path.split('/')[-1]}",
                "Content-Type": "application/octet-stream"
            }
            return Response(content=file_content, headers=headers)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"File not found: {e}"
        )
