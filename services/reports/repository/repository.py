from typing import List

import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import desc, update
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert

from services.objects.models.objects import ObjectModel
from services.reports.schemes.reports import Reports, ReportsListRs, ReportsGetRs, Construction, Safety
from services.reports.models.reports import ReportModel
from core.settings import settings
from utils.get_s3_urls import generate_files_dict


class ReportsRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_object_info(
            self,
            object_id: str
    ) -> List:
        result = await self.db_session.execute(
            select(
                ObjectModel.name,
                ObjectModel.reports_count
            )
            .where(
                ObjectModel.id == object_id
            )
        )
        response = result.fetchall()[0]
        return response

    async def update_reports_count(
            self,
            object_id: str,
            reports_count: int
    ):
        await self.db_session.execute(
            update(ObjectModel)
            .where(ObjectModel.id == object_id)
            .values(reports_count=reports_count)
        )
        await self.db_session.commit()


    async def create(
            self,
            report_id: int,
            object_id: str,
            num: int,
            prediction_amount: int,
            types_amount: int,
            count_person: int,
            count_person_with_helmet: int,
            count_person_without_helmet: int,
            count_person_violations: int,
            count_construction_violations: int
    ):
        stmt = insert(ReportModel).values(
            uuid=str(uuid.uuid4()),
            id=report_id,
            object_id=object_id,
            photo_amount=num,
            known_amount=prediction_amount,
            types_amount=types_amount,
            workers_amount=count_person,
            good_workers_amount=count_person_with_helmet,
            bad_workers_amount=count_person_without_helmet,
            workers_violation_amount=count_person_violations,
            object_violation_amount=count_construction_violations,
            is_safe=1 if count_person_violations == 0 and count_construction_violations == 0 else 0
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()

    async def list(
            self,
            object_id: str
    ) -> ReportsListRs:
        result = await self.db_session.execute(
            select(
                ReportModel.id,
                ReportModel.created_at,
                ReportModel.photo_amount,
                ReportModel.is_safe
            )
            .order_by(
                desc(ReportModel.id)
            )
            .where(
                ReportModel.object_id == object_id
            )
        )
        reports = result.fetchall()

        response = []
        for report in reports:
            response.append(
                Reports(
                    id=report.id,
                    created_at=report.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    photo_amount=report.photo_amount,
                    is_safe=report.is_safe
                )
            )

        return ReportsListRs(
            reports=response
        )

    async def get(
            self,
            object_id: str,
            report_id: int
    ) -> ReportsGetRs:
        object_name = await self.get_object_info(object_id)
        result = await self.db_session.execute(
            select(
                ReportModel.created_at,
                ReportModel.photo_amount,
                ReportModel.known_amount,
                ReportModel.types_amount,
                ReportModel.workers_amount,
                ReportModel.good_workers_amount,
                ReportModel.bad_workers_amount,
                ReportModel.workers_violation_amount,
                ReportModel.object_violation_amount,
                ReportModel.is_safe
            )
            .where(
                ReportModel.object_id == object_id,
                ReportModel.id == report_id
            )
        )
        report = result.fetchall()[0]

        urls = await generate_files_dict(
            bucket_name=settings.minio_bucket,
            base_prefix=f"{object_id}/{report_id}/"
        )

        print(urls)
        return ReportsGetRs(
            object_name=object_name[0],
            created_at=report.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            photo_amount=report.photo_amount,
            construction_report=Construction(
                known_amount=report.known_amount,
                types_amount=report.types_amount,
                completeness=int(report.known_amount / report.types_amount)
            ),
            safety_report=Safety(
                workers_amount=report.workers_amount,
                good_workers_amount=report.good_workers_amount,
                bad_workers_amount=report.bad_workers_amount,
                workers_violation_amount=report.workers_violation_amount,
                object_violation_amount=report.object_violation_amount,
                is_safe=report.is_safe
            ),
            urls=urls,
        )
