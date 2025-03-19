from typing import List

from pydantic import BaseModel

class Objects(BaseModel):
    id: str
    name: str

class ObjectsListRs(BaseModel):
    objects: List[Objects]


class ObjectsCreateRs(BaseModel):
    status: str


class ObjectsCreateRq(BaseModel):
    name: str
