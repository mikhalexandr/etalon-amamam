from sqlalchemy.ext.asyncio import AsyncSession

from services.objects.repository.repository import ObjectsRepository
from services.objects.schemes.objects import ObjectsListRs, ObjectsCreateRs, ObjectsCreateRq


# Usecase отвечает за бизнес-логику объектов
class ObjectsUseCase:
    # Инициализация
    def __init__(self, db_session: AsyncSession):
        self.repository = ObjectsRepository(db_session)

    # Создание объекта
    async def create(
            self,
            request: ObjectsCreateRq
    ) -> ObjectsCreateRs:
        return await self.repository.create(request)

    # Получение списка объектов
    async def list(
            self
    ) -> ObjectsListRs:
        return await self.repository.list()
