from minio import Minio
from core.logger import logger
from core.settings import settings


class MinioClient:
    _client = None

    @classmethod
    def init_minio(cls) -> None:
        if cls._client is not None:
            logger.error("Minio is already initialized")
            return None

        cls._client = Minio(
            settings.minio_url,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure
        )
        logger.info("Minio initialized")


    @classmethod
    def close_minio(cls) -> None:
        if cls._client is not None:
            cls._client = None
            logger.info("Minio closed")

    @classmethod
    def get_minio(cls):
        return cls._client
