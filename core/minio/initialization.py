from aiobotocore.session import get_session

from core.logger import logger
from core.settings import settings


class MinioClient:
    _client = None

    @classmethod
    async def init_minio(cls) -> None:
        if cls._client is not None:
            logger.error("Minio is already initialized")
            return None

        session = get_session()
        cls._client = session.create_client(
            's3',
            endpoint_url=settings.minio_url,
            aws_access_key_id=settings.minio_access_key,
            aws_secret_access_key=settings.minio_secret_key,
            region_name='us-east-1',
            use_ssl=settings.minio_secure
        )
        logger.info("Minio initialized")

    @classmethod
    async def close_minio(cls) -> None:
        if cls._client is not None:
            cls._client = None
            logger.info("Minio closed")

    @classmethod
    def get_minio(cls):
        return cls._client
