import uuid

from repositories.event_type import EventTypeRepository
from exceptions import ConflictException, NotFoundException


class EventTypeUseCase:
    def __init__(self, repo: EventTypeRepository):
        self.repo = repo

    async def list_all(self):
        return await self.repo.list_all()

    async def get_by_id(self, event_type_id: uuid.UUID):
        event_type = await self.repo.get_by_id(event_type_id)
        if not event_type:
            raise NotFoundException("EventType not found")
        return event_type

    async def create(self, title: str, description: str | None, duration_minutes: int):
        from models.event_type import EventType
        event_type = EventType(
            title=title,
            description=description,
            duration_minutes=duration_minutes,
        )
        return await self.repo.create(event_type)

    async def update(self, event_type_id: uuid.UUID, title: str | None, description: str | None, duration_minutes: int | None):
        event_type = await self.get_by_id(event_type_id)
        data = {}
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if duration_minutes is not None:
            data["duration_minutes"] = duration_minutes
        return await self.repo.update(event_type, data)

    async def delete(self, event_type_id: uuid.UUID):
        event_type = await self.get_by_id(event_type_id)
        has_bookings = await self.repo.has_bookings(event_type_id)
        if has_bookings:
            raise ConflictException("Cannot delete EventType with existing bookings")
        await self.repo.delete(event_type)