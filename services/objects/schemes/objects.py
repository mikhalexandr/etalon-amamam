from typing import List

from pydantic import BaseModel


class ObjectsCreateRq(BaseModel):
    name: str


class ObjectsCreateRs(BaseModel):
    status: str


class Objects(BaseModel):
    id: str
    name: str


class ObjectsListRs(BaseModel):
    objects: List[Objects]
