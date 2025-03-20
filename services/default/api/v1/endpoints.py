from datetime import datetime

from fastapi import APIRouter

from services.default.schemes.default import DefaultRootRs, DefaultPingRs

router = APIRouter(
    tags=["default"]
)


# Роутер по умолчанию
@router.get(
    "/",
    response_model=DefaultRootRs,
)
async def root() -> DefaultRootRs:
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return DefaultRootRs(
        status="OK",
        current_time=current_time
    )


# Роутер для проверки работоспособности сервера
@router.get(
    "/api/ping",
    response_model=DefaultPingRs
)
async def ping() -> DefaultPingRs:
    return DefaultPingRs(
        status="pong"
    )
