from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from core.settings import settings
from core.logger import init_logger, logger
from core.postgres.initialization import PostgresClient
from core.redis.initialization import RedisClient
from core.roboflow.initialization import RoboflowClient
from services import init_routers


class LimitUploadSize(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_upload_size: int) -> None:
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.method == 'POST':
            if 'content-length' not in request.headers:
                return Response(status_code=status.HTTP_411_LENGTH_REQUIRED)
            content_length = int(request.headers['content-length'])
            if content_length > self.max_upload_size:
                return Response(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        return await call_next(request)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_logger()
    await PostgresClient.init_postgres()
    await RedisClient.init_redis()
    await RoboflowClient.init_roboflow()
    logger.info("All resources have been successfully initialized")
    yield
    await PostgresClient.close_postgres()
    await RedisClient.close_redis()
    await RoboflowClient.close_roboflow()
    logger.info("All resources have been successfully closed")

def init_app() -> FastAPI:
    _app = FastAPI(
        title="Etalon API",
        version="1.0.0",
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        lifespan=lifespan,
    )
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.add_middleware(LimitUploadSize, max_upload_size=300_000_000)
    init_routers(_app)
    return _app

app = init_app()

if __name__ == "__main__":
    host, port = settings.server_address.split(":")
    uvicorn.run(app, host=host, port=int(port))
