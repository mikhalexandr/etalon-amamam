from typing import List

import redis.asyncio as redis
from fastapi import File, UploadFile
from inference_sdk import InferenceHTTPClient
from sqlalchemy.ext.asyncio import AsyncSession

from services.reports.repository.repository import ReportsRepository
from services.reports.schemes.reports import ReportsCreateRs, ReportsListRs, ReportsGetRs
from utils.generate_photos import process_photo
from utils.generate_txt_files import process_txt


class ReportsUseCase:
    def __init__(
            self,
            db_session: AsyncSession,
            redis_client: redis.Redis = None,
            roboflow_client: InferenceHTTPClient = None
    ):
        self.repository = ReportsRepository(db_session)
        self.redis_client = redis_client
        self.roboflow_client = roboflow_client

    async def create(
            self,
            object_id: str,
            files: List[UploadFile] = File(...),
    ) -> ReportsCreateRs:
        name, reports_count = await self.repository.get_object_info(object_id)
        reports_count += 1
        time = 0
        predictions_amount = 0
        types_amount = 0
        predictions = {}
        count_person_violations = 0
        count_construction_violations = 0
        count_person_with_helmet = 0
        count_person_without_helmet = 0
        count_person = 0
        filtered_boxes = {}
        num = 0
        for file in files:
            num += 1
            content = await file.read()
            result = await process_photo(
                num,
                object_id,
                content,
                reports_count,
                self.redis_client,
                self.roboflow_client
            )
            time += result['time']
            predictions_amount += result['predictions_amount']
            types_amount += result['types_amount']
            if 'predictions' in result and len(result['predictions']) > 0:
                predictions[f"Photo {num}"] = result['predictions']
            count_person_violations += result['count_person_violations']
            count_construction_violations += result['count_construction_violations']
            count_person_with_helmet += result['count_person_with_helmet']
            count_person_without_helmet += result['count_person_without_helmet']
            count_person += result['count_person']
            print(result['filtered_boxes'])
            if 'filtered_boxes' in result and len(result['filtered_boxes']) > 0:
                filtered_boxes[f"Photo {num}"] = result['filtered_boxes']
        await process_txt(
            object_id,
            name,
            reports_count,
            num,
            time,
            predictions_amount,
            types_amount,
            predictions,
            count_person_violations,
            count_construction_violations,
            count_person_with_helmet,
            count_person_without_helmet,
            count_person,
            filtered_boxes,
        )
        await self.repository.create(
            reports_count,
            object_id,
            num,
            predictions_amount,
            types_amount,
            count_person,
            count_person_with_helmet,
            count_person_without_helmet,
            count_person_violations,
            count_construction_violations,
        )
        await self.repository.update_reports_count(object_id, reports_count)
        return ReportsCreateRs(
            status="OK"
        )

    async def list(
            self,
            object_id: str
    ) -> ReportsListRs:
        return await self.repository.list(object_id)

    async def get(
            self,
            object_id: str,
            report_id: int
    ) -> ReportsGetRs:
        return await self.repository.get(object_id, report_id)
