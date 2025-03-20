from inference_sdk import InferenceHTTPClient

from core.logger import logger
from core.settings import settings


# Инициализация Roboflow
class RoboflowClient:
    _client: InferenceHTTPClient | None = None

    @classmethod
    async def init_roboflow(cls) -> None:
        if cls._client is not None:
            logger.error("Roboflow is already initialized")
            return None

        cls._client = InferenceHTTPClient(
            api_url=settings.roboflow_api_url,
            api_key=settings.roboflow_api_key
        )
        logger.info("Roboflow initialized")

    @classmethod
    async def close_roboflow(cls) -> None:
        if cls._client is not None:
            logger.info("Roboflow closed")
            cls._client = None

    @classmethod
    def get_roboflow(cls) -> InferenceHTTPClient:
        return cls._client
