from pydantic import BaseModel


# Схема для корневого ответа
class DefaultRootRs(BaseModel):
    status: str
    current_time: str


# Схема для пинга
class DefaultPingRs(BaseModel):
    status: str
