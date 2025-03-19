from aiobotocore.session import get_session

from core.minio.initialization import MinioClient


async def get_minio() -> get_session:
    return MinioClient.get_minio()
