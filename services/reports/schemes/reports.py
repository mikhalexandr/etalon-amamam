from typing import Dict, List

from pydantic import BaseModel


class ReportsCreateRs(BaseModel):
    report_id: int


class Reports(BaseModel):
    id: int
    created_at: str
    completeness: int
    is_safe: int


class ReportsListRs(BaseModel):
    reports: List[Reports]


class Construction(BaseModel):
    known_amount: int
    types_amount: int
    completeness: int


class Safety(BaseModel):
    workers_amount: int
    good_workers_amount: int
    bad_workers_amount: int
    workers_violation_amount: int
    object_violation_amount: int
    is_safe: int


class ReportsGetRs(BaseModel):
    object_name: str
    created_at: str
    photo_amount: int
    construction_report: Construction
    safety_report: Safety
    urls: Dict[str, List[str]]
