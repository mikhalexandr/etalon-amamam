import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import desc
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert

from services.objects.schemes.objects import ObjectsListRs, ObjectsCreateRs, ObjectsCreateRq
from services.objects.models.objects import ObjectModel


class ObjectsRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def list(
            self
    ) -> ObjectsListRs:
        result = await self.db_session.execute(
            select(
                ObjectModel.id,
                ObjectModel.name
            )
            .order_by(
                desc(ObjectModel.updated_at)
            )
        )
        objects = result.fetchall()

        response = []
        for object_ in objects:
            response.append(
                {
                    "id": object_[0],
                    "name": object_.name
                }
            )

        return ObjectsListRs(
            objects=response
        )

    async def create(
            self,
            request: ObjectsCreateRq
    ) -> ObjectsCreateRs:
        name = request.name
        id_ = str(uuid.uuid4())

        stmt = insert(ObjectModel).values(
            id=id_,
            name=name
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()

        return ObjectsCreateRs(
            status="OK"
        )
