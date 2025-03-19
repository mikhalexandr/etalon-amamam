from pydantic import BaseModel


class DefaultRootRs(BaseModel):
    status: str
    current_time: str


class DefaultPingRs(BaseModel):
    status: str
